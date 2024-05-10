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

#mpirun python src/main_str.py data/390.pdf ttt

srun --mpi=pmi2 python src/main_scatter.py data/390.pdf ttt >> results/slurm/srun.txt
# srun --mpi=pmi python src/main_scatter.py data/390.pdf data/391.pdf ttt


serial_dir="results/serial_out"
worker_dir="results/worder_out"
scatter_dir="results/scatter_out"
output_txt="results/slurm/srun.txt"
output_csv="results/slurm/srun.csv"

if [[ $# -ne '1' ]]; then
    echo "Usage:" $0 "<pdf-directory>"
    exit 1
fi

# Find all pdf filtes to tests with
pdfs=()
for pdf_file in $1/*.pdf; do
    pdfs+=" "
    pdfs+=$pdf_file
done
mkdir -p results
echo "" > "$output_txt"

# Step through different number of porcersses
sizes=(2 4 8 16)
for size in "${sizes[@]}"; do
    rm -rf $worker_dir # Delete old outputs so that file and directory creation times are included
    echo "=== Workers Parallel ===" >> "$output_txt"
    srun --mpi=pmi2 -n $size python src/main_str.py ${pdfs} $worker_dir >> results/slurm/srun.txt

    rm -rf $scatter_dir # Delete old outputs so that file and directory creation times are included
    echo "=== Scatter Parallel ===" >> "$output_txt"
    srun --mpi=pmi2 -n $size python src/main_scatter.py ${pdfs} $scatter_dir >> results/slurm/srun.txt

done

# Write results to a csv for analysis
python write2csv.py "$output_txt" "$output_csv"