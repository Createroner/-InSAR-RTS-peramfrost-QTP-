#!/bin/bash
#SBATCH -J InSAR 
#SBATCH -p Long
#SBATCH -t 3-00:00:00 
#SBATCH -N 1 
#SBATCH -c 40 
#SBATCH --mem=256G 
#SBATCH --exclusive 
#SBATCH -o log/%j.job
echo ---------start---------
# cd beiluhe2

#mkdir saf_d169_proc

#cd saf_d169_proc

#cp /work/yxtang/zlc/beiluhe_sig.sh ./

module load container/singularity/singularity-3.5.3

frame=$1

singularity exec --bind /work/yxtang/zlc:/data /work/yxtang/zlc/mint.sif bash sentinel_sig.sh $frame




echo ---------end---------
