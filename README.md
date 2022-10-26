# Cryo-EM Synthethic Generation
Notion notebook: https://glimmer-brie-6b7.notion.site/NLRP3-Simulation-Experiment-dbdca9c949ed45328ed2d1f312a3cf99

## Refence
- Seitz, E., Acosta-Reyes, F., Schwander, P., & Frank, J. (2019). Simulation of cryo-EM ensembles from atomic models of molecules exhibiting continuous conformations.https://www.biorxiv.org/content/10.1101/864116v1. (github: https://github.com/evanseitz/cryoEM_synthetic_generation)

- ManifoldEM: https://github.com/evanseitz/ManifoldEM_Python

## Softwares and how to use:
See the details of downloading in the Notion notebook appendix.
- Chimera (UCSF): `Chimera --nogui .py`.
- Phenix: `source phenix_env.sh` before run the bash script.
- EMAN2: Activate conda before run the bash script.
- RELION: **Deactivate** conda before run the bash script.

## Python environment:
Use ManifoldEM environment for every python script. 

`conda create env -f ManifoldEM_env_linux.yml`



