import os, os.path, sys
import numpy as np
import itertools
import matplotlib
import matplotlib.pyplot as plt
from pylab import imshow, show, loadtxt
import mrcfile
import csv
import re
from scipy import stats
from decimal import Decimal

# Select #PDs and SNR
selPDs = 30
selSNR = 0.1


pyDir = os.path.dirname(os.path.abspath(__file__)) #python file directory
parDir = os.path.dirname(pyDir) #parent directory
dataDir = os.path.join(parDir, '4_Projection/stacks') #location of all .star and .mrcs
occFile = os.path.join(parDir, '3_Occupancies/3CM_20states.npy')
#output file
fname = f'NLRP3_{selPDs}PDs_SNR' + f'{selSNR}'.replace(".", "")
stackOut = os.path.join(parDir, '%s.mrcs' % fname)
alignOut = os.path.join(parDir, '%s.star' % fname)

if os.path.exists(stackOut):
    os.remove(stackOut)
if os.path.exists(alignOut):
    os.remove(alignOut)

occ = np.load(occFile)
# Load one stack to check the dim
tempPath = os.path.join(dataDir, sorted(os.listdir(dataDir))[0])
#print(tempPath)
temp_stack = mrcfile.open(tempPath)
PDs, box, box = temp_stack.data.shape
temp_stack.close
PDs = selPDs #comment this line out for full stack
snapshots = int(np.sum(occ)*PDs)
print('Snapshots:',snapshots)

starPaths = []
for root, dirs, files in os.walk(dataDir):
    for file in sorted(files):
        if not file.startswith('.'): #ignore hidden files
            if file.endswith(".star"):
                starPaths.append(os.path.join(root, file))

stackPaths = []
for root, dirs, files in os.walk(dataDir):
    for file in sorted(files):
        if not file.startswith('.'): #ignore hidden files
            if file.endswith(".mrcs"):
                stackPaths.append(os.path.join(root, file))
    
##########################
# FUNCTIONS:
########################## 
# function to find SNR:
def find_SNR(image):
    IMG_2D = []
    for pix in image:
        IMG_2D.append(pix)

    IMG_1D = list(itertools.chain.from_iterable(IMG_2D))
    img_mean = np.mean(IMG_1D)
    img_var = np.var(IMG_1D)
    img_std = np.sqrt(img_var)
    
    if 0: #to illustrate signal only, must be OFF during stack generation
        SIG_1D = np.ndarray(shape=np.shape(IMG_1D)) #empty array for signal-pixels only
        idx = 0
        for pix in IMG_1D:
            #if -img_std*.25 < pix < img_std*.25:
            if (img_mean-img_std*.5) < pix < (img_mean+img_std*.5):
                SIG_1D[idx] = -100 #arbitrarily large for illustration
            else:
                SIG_1D[idx] = IMG_1D[idx]
            idx += 1
        SIG_2D = np.asarray(SIG_1D).reshape(320, 320)
        plt.imshow(SIG_2D)
        plt.show()
        
    else:
        SIG_1D = []
        for pix in IMG_1D:
            if -img_std*.25 < pix < img_std*.25:
                pass
            else:
                SIG_1D.append(pix) #only grab signal

    sig_mean = np.mean(SIG_1D)
    sig_var = np.var(SIG_1D)
    noise_var = sig_var / selSNR # Determain SNR
    noise_std = np.sqrt(noise_var)
    
    return sig_mean, noise_std

##########################
# function to add noise:
def add_noise(mean, std, image):
    row, col = image.shape
    gauss = np.random.normal(mean, std, (row, col))
    gauss = gauss.reshape(row, col)
    noisy = image + gauss
    return noisy

##########################
# function to normalize:
def normalize(image):
    bg = []
    h, w = image.shape[:2]
    center = [int(w/2), int(h/2)]
    radius = int(h/2)
    Y, X = np.ogrid[:h,:w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y - center[1])**2)
    mask = dist_from_center <= radius
    masked_img = image.copy()
    if 0: #for visualization of mask only, keep off (0)
        masked_img[~mask] = 0
        plt.imshow(masked_img, cmap='gray')
        plt.show()
    bg = masked_img[~mask]
    bg_mean = np.mean(bg)
    bg_std = np.std(bg)
    img_norm = (image - bg_mean) / bg_std
    if 0: #NORM CHECK, for testing only
        print('bg_mean:', bg_mean)
        print('bg_std:', bg_std)
    return img_norm

##########################
# PREPROCESSING:
##########################
# (danlin) Remove \n \ after \nloop_ \ for using cryodrgn transform .star to .pkl
# initiate alignment file:
alignFile = open(alignOut, 'w')
alignFile.write('\ndata_ \
                \n \
                \nloop_ \
                \n_rlnAngleRot #1 \
                \n_rlnAngleTilt #2 \
                \n_rlnAnglePsi #3 \
                \n_rlnOriginX #4 \
                \n_rlnOriginY #5 \
                \n_rlnDefocusU #6 \
                \n_rlnDefocusV #7 \
                \n_rlnVoltage #8 \
                \n_rlnSphericalAberration #9 \
                \n_rlnAmplitudeContrast #10 \
                \n_rlnDefocusAngle #11 \
                \n_rlnCtfBfactor #12 \
                \n_rlnPhaseShift #13 \
                \n_rlnPixelSize #14 \
                \n_rlnImageName #15 \
                \n')



##########################
# create empty arrays:
img_array = mrcfile.new_mmap(stackOut, shape=(snapshots,box,box), mrc_mode=2, overwrite=True) #mrc_mode 2: float32

##########################
# INITIATE MAIN LOOP:
##########################
# import original stacks:
idx = 0 #index for stack/stars
img = 0 #index for every individual image in new stack
np.random.seed(915)
PD_select = np.random.randint(0,362,size=PDs)
for z in stackPaths:
    stack = mrcfile.open(z)
    starPath = starPaths[idx]
        
    starFile = []
    with open(starPath, 'r') as values: 
        for i in range(0,19): #skip header
            next(values)
        starReader = csv.reader(values)
        for lines in starReader:
            starFile.append(lines)
    values.close()
    
    #for PD in range(len(stack.data)): #e.g., [0,812]
    for PD in PD_select: #comment out for full stack and use above line instead
        #star = re.split(r'[ ,|;"]+', starFile[PD+1][0]) #doesn't catch scientific notation
        star = starFile[PD+1][0].split() #skip by spacing; need to make sure skipping header correctly 

        img_orig = stack.data[PD] #each image within a given stack; e.g. len = 812
        
        sig_mean, noise_std = find_SNR(img_orig) #find SNR
        img_noise = add_noise(sig_mean, noise_std, img_orig) #apply noise
        img_norm = normalize(img_noise) #normalize

        
        img_array.data[img] = img_norm
        
        
        if 0:
            print('norm check:')
            normalize(img_norm) #NORM CHECK
        
        #############################
        # update alignment file:
        alignFile.write('%.6f\t%.6f\t%.6f\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s@%s.mrcs\n' \
            % (Decimal(star[0]), Decimal(star[1]), Decimal(star[2]), float(star[3]), float(star[4]), \
            float(star[5]), float(star[6]), float(star[7]), float(star[8]), float(star[9]), \
            float(star[10]), float(star[11]), float(star[12]), float(star[13]), int(img+1), str(fname)))

        img += 1
        print('%s / %s' % (img, snapshots))
    
    
    idx += 1
    stack.close()
    
alignFile.close()
    
print('All Processes Complete')
