for i in /home/danlin/synth_cryoEM/3_Occupancies/MRC_clones/*.mrc
do
    out=`basename $i`
    angFile=/home/danlin/synth_cryoEM/4_Projection/STARs/proj812_${out%.*}.star
    outFile=/home/danlin/synth_cryoEM/4_Projection/stacks/${out%.*}
    echo $outFile
    relion_project --i "${i}" --o $outFile --ang $angFile --ctf true --angpix 1
done
