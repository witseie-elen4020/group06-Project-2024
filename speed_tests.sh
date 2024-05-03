#!/bin/bash
# An ALternative to slurm wich seems to be faster for parallel processing

# Note - there are 20 compute nodes each with 4 cores and 32 GB mem
# ntasks above is the number of cores - 40 is half the cluster, 80 is full
# If running long jobs rather use 20 - 40 to leave capacity for others
# exec srun --unbuffered --mpi=pmi2 /usr/bin/python3 src/dotProductParallel.py 40 1000
# Define an array of array sizes

serial_dir="results/serial_out"
worker_dir="results/worder_out"
scatter_dir="results/scatter_out"
output_txt="results/times.txt"

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

echo "" > "$output_txt"

# Get serial banchmark
rm -rf $serial_dir # Delete old outputs so that file and directory creation times are included
python3 src/main_serial.py ${pdfs} $serial_dir >> "$output_txt"

# Step through different number of porcersses
sizes=(2 4 8 16)
for size in "${sizes[@]}"; do
    rm -rf $worker_dir # Delete old outputs so that file and directory creation times are included
    echo "=== Workers Parallel ===" >> "$output_txt"
    mpiexec -n $size python3 src/main_str.py ${pdfs} $worker_dir >> "$output_txt"

    rm -rf $scatter_dir_dir # Delete old outputs so that file and directory creation times are included
    echo "=== Scatter Parallel ===" >> "$output_txt"
    mpiexec -n $size python3 src/main_scatter.py ${pdfs} $scatter_dir >> "$output_txt"
done
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
