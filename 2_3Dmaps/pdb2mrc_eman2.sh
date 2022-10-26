# script to convert all re-centered PDBs into MRCs (`_1.mrc` represents the 1st copy of each)

for i in /home/danlin/synth_cryoEM/1_CMs/align_CMs/*.pdb
do
    out=`basename ${i%.*}_1.mrc`
    outFile=/home/danlin/synth_cryoEM/2_3Dmaps/MRCs/$out
    echo "$outFile"
    e2pdb2mrc.py "${i}" $outFile -A 1 -R 3 -B 128 #pixel size, resolution, box size (box size was originally 320)
done
