import os, os.path, sys
import shutil
import numpy as np
import cv2
import itertools
import matplotlib
import matplotlib.pyplot as plt
from pylab import imshow, show, loadtxt
import mrcfile
from scipy.fftpack import ifftshift
from scipy.fftpack import fft2
from scipy.fftpack import ifft2
import csv
import pandas as pd

# required environment = ManifoldEM

##########################
# user inputs:
pyDir = os.path.dirname(os.path.abspath(__file__)) #python file directory
parDir = os.path.dirname(pyDir) #parent directory
origDir = os.path.join(parDir, '2_3Dmaps/MRCs')
occPath = os.path.join(pyDir, '3CM_20states.npy')
cloneDir = os.path.join(pyDir, 'MRC_clones')

occFile = np.load(occPath)
states = 20

occ = []
for i in range(1, states+1):
    for j in range(1, states+1): 
        for k in range(1, states+1):
            occ.append(occFile[k-1][j-1][i-1])
	
occMax = int(np.amax(occ))
	
fnames = []
for filename in os.listdir(origDir):
    if filename.endswith('.mrc'):
        fnames.append(filename)
#fnames.sort(key=lambda f: int(filter(str.isdigit, f))) #Python2
fnames.sort(key=lambda f: list(filter(str.isdigit, f))) #Python3; i.e., https://www.py4u.net/discuss/173770

idx = 0
for i in fnames:
    if occ[idx] == 0:
        idx += 1
    else:
        short = i[:-4]
        new1 = short + ('_%02d.mrc' % 1)
        shutil.copy('%s/%s' % (origDir,i), '%s/%s' % (cloneDir,new1))
        print(i)
        for j in range(2,occMax+1):
            if occ[idx] >= j:
                #short = i[:-4]
                #print(short)
                new = short + ('_%02d.mrc' % j)
                shutil.copy('%s/%s' % (origDir,i), '%s/%s' % (cloneDir,new))
        idx += 1
print(sum(occ),"MRCs")