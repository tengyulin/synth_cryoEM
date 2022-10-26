# script to re-center all PDBs based on common center-of-mass coordinates

for i in /home/danlin/synth/1_CMs/CMs/*.pdb
do
    out=`basename $i`
    outFile=/home/danlin/synth/1_CMs/align_CMs/$out
    echo "$outFile"
    phenix.pdbtools "${i}" output.file_name=$outFile sites.translate="-105.95 -104.70 -104.87" #replace with CoM of your pdb
done

