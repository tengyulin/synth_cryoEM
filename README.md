# Cryo-EM Synthethic Generation
Notion notebook: https://glimmer-brie-6b7.notion.site/NLRP3-Simulation-Experiment-dbdca9c949ed45328ed2d1f312a3cf99

Refence: Simulation of Cryo-EM Ensembles from Atomic Models of Molecules Exhibiting Continuous Conformations (Seitz, Acosta-Reyes, Schwander, Frank): https://www.biorxiv.org/content/10.1101/864116v1. (github:https://github.com/evanseitz/cryoEM_synthetic_generation )

## Softwares and how to use:
See the details of downloading in the Notion notebook appendix.
- Chimera (UCSF): `Chimera --nogui .py`.
- Phenix: `source phenix_env.sh` first, then run the bash script by `sh shiftPDB.sh`
- EMAN2: Activate conda before run the bash script.
- RELION: **Deactivate** conda before run the bash script.

## Python environment:
Use ManifoldEM environment for every python script. 

`conda create env -f ManifoldEM_env_linux.yml`



