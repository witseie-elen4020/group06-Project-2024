#!/bin/bash
#SBATCH --job-name=srun_speed_tests
#SBATCH --output=results/slurm/srun.txt
#SBATCH --error=results/slurm/srun_error.txt
#SBATCH --cpus-per-task=1
#SBATCH --ntasks=16


# This script is used to create an run a slurm batch of tests on the cluster.
# The full number of tasks tested (16) are requested however the number of tasks allocated to each execution is varied
# Each extraction operation if perfoemd five times becuase timing results are increadibly variable

export SLURM_CPU_BIND=None

# Note - there are 20 compute nodes each with 4 cores and 32 GB mem
# ntasks above is the number of cores - 40 is half the cluster, 80 is full
# If running long jobs rather use 20 - 40 to leave capacity for others
# exec srun --unbuffered --mpi=pmi2 /usr/bin/python3 src/dotProductParallel.py 40 1000
# Define an array of array sizes

serial__dir="results/serial_out"
worker_dir="results/worder_out"
scatter_dir="results/scatte_out"


# Delete output directory so that time taken to make files is accuratly recorded 
rm -rf $serial__dir
rm -rf $worker_dir
rm -rf $scatter_dir

#mpirun python src/main_str.py data/390.pdf ttt
srun --unbuffered --mpi=pmi2 python src/main_scatter.py data/390.pdf ttt >> results/slurm/srun.txt

srun --mpi=pmi2 python src/main_scatter.py data/390.pdf ttt >> srun.txt
# srun --mpi=pmi python src/main_scatter.py data/390.pdf data/391.pdf ttt

