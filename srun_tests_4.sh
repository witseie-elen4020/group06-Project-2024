#!/bin/bash
#SBATCH --job-name=srun_tests_4
#SBATCH --output=parallel_4.txt
#SBATCH --error=parallel_4_error.txt
#SBATCH --cpus-per-task=1
#SBATCH --ntasks=16

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

exec srun --unbuffered --mpi=pmi2 /usr/bin/python3 src/main_str.py data/390.pdf ttt
# mpirun -n 8 /usr/bin/python3 src/main_str.py data/390.pdf ttt
# mpirun -n 16 /usr/bin/python3 src/main_str.py data/390.pdf ttt


# Define array of array sizes and cycles
array_sizes=(20 40 200 400 2000 4000)
cycles=100

# # Print a header to the output file to distinguish outputs
# echo "---- dotProductParallel Python Outputs ----" >> combined_output_%j.txt
# # Execute the dotProductParallel Python script
# for size in "${array_sizes[@]}"; do
#     #echo "Running dotProductParallel.py with size $size and cycles $cycles" >> combined_output_%j.txt
#     srun --unbuffered --mpi=pmi2 /usr/bin/python3 src/dotProductParallel.py $size $cycles >> combined_output_%j.txt 2>&1
#     echo "----------------------------------------------------" >> combined_output_%j.txt
# done
