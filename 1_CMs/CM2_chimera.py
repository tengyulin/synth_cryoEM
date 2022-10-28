import os
from chimera import runCommand as rc

# INSTRUCTIONS: run this file from same directory as your PDB file are located... 
	# CM1 states will output to CMs folder

pyDir = os.path.dirname(os.path.abspath(__file__)) #python file location
parDir = os.path.abspath(os.path.join(pyDir, os.pardir))
cm1Dir = os.path.join(pyDir, 'CM1')
outDir = os.path.join(pyDir, 'CM2')

cm1Paths = []
for root, dirs, files in os.walk(cm1Dir):
    for file in sorted(files):
        if not file.startswith('.'): #ignore hidden files
            if file.endswith(".pdb"):
                cm1Paths.append(os.path.join(root, file))

mov = 0.5
for cm1 in cm1Paths:
    outName = os.path.basename(cm1)[:-4] # remove .pdb filename
    rc('open' + cm1)
    rc('split #0') # chain A_head #0.1; chian B # 0.2; chain A_tail #0.3 
    for j in range(1,11):
        if j == 1: #don't move for state 1
            rc('combine #0') # combine model would be #1
            rc('write relative #0.1 format pdb #1 %s/%s_0%s.pdb' % (outDir,outName,j))
        else:
            rc('move 0,1,1 %f models #0.2 coord #0.3' % mov) #B move toward A 
            rc('combine #0')
            if j < 10:
                rc('write relative #0.1 format pdb #1 %s/%s_0%s.pdb' % (outDir,outName,j))
            else:
                rc('write relative #0.1 format pdb #1 %s/%s_%s.pdb' % (outDir,outName,j))
        rc('close #1')
    rc('close #0')