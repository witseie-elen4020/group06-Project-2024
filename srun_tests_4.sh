#!/bin/bash
#SBATCH --job-name=srun_tests_4
#SBATCH --output=parallel_4.txt
#SBATCH --error=parallel_4_error.txt
#SBATCH --cpus-per-task=1
#SBATCH --ntasks=4

# https://stackoverflow.com/questions/31848608/slurms-srun-slower-than-mpirun

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

mpiexec -n 4 python src/main_str.py data/390.pdf ttt
# srun --mpi=pmi python src/main_scatter.py data/390.pdf ttt
# srun --mpi=pmi python src/main_scatter.py data/390.pdf data/391.pdf ttt

