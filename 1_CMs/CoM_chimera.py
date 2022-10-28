import os
from chimera import runCommand as rc

# Calculate center of mass using chimera 

pyDir = os.path.dirname(os.path.abspath(__file__)) #python file location
ref_state = os.path.join(pyDir, 'CM2/state_01_01.pdb') 
# Since our aim is center every .pdb file, we could choose any state we genertated.

rc('open' + ref_state)
rc('measure center #0')