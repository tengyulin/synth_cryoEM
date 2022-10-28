import os
from chimera import runCommand as rc

# INSTRUCTIONS: run this file from same directory as your PDB file are located... 
	# CM1 states will output to CMs folder

pyDir = os.path.dirname(os.path.abspath(__file__)) #python file location
parDir = os.path.abspath(os.path.join(pyDir, os.pardir))
outDir = os.path.join(pyDir, 'CM1')
A_head = os.path.join(pyDir, 'A.1.pdb')
A_tail = os.path.join(pyDir, 'A.2.pdb')
B_ball = os.path.join(pyDir, 'B.pdb')

rc('open' + A_head) # model #0
rc('open' + A_tail) # model #1
rc('open' + B_ball) # model #2

rot = .5 
for i in range(1,21): # numbers of states to generate
    if i == 1: #don't rotate for state 1
        rc('combine #0-2, name state_%s' % i) # combine model would be #3
        rc('write relative #1 format pdb #3 %s/state_0%s.pdb' % (outDir,i))
    else:
        rc('turn 0,0,1 %f center #0:653 models #0' % rot) # split point #0:653 as rotation center
        rc('combine #0-2, name state_%s' % i)
        if i < 10:
            rc('write relative #1 format pdb #3 %s/state_0%s.pdb' % (outDir,i))
        else:
            rc('write relative #1 format pdb #3 %s/state_%s.pdb' % (outDir,i))
    rc('close #3') # close combine model
