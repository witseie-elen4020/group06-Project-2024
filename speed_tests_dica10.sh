#!/bin/bash
# Similar to the orignal speed tests script but run on dica10 to investage scaling with 12 cores

# Note - there are 20 compute nodes each with 4 cores and 32 GB mem
# ntasks above is the number of cores - 40 is half the cluster, 80 is full
# If running long jobs rather use 20 - 40 to leave capacity for others
# exec srun --unbuffered --mpi=pmi2 /usr/bin/python3 src/dotProductParallel.py 40 1000
# Define an array of array sizes

serial_dir="results/serial_out"
worker_dir="results/worker_out"
scatter_dir="results/scatter_out"
output_txt="results/times_dica10.txt"
output_csv="results/times_dica10.csv"

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

# Get serial banchmark
rm -rf $serial_dir # Delete old outputs so that file and directory creation times are included
echo "=== Serial ===" >> "$output_txt"
python src/main_serial.py ${pdfs} $serial_dir >> "$output_txt"

# Step through different number of porcersses
sizes=(2 4 8 12)
for size in "${sizes[@]}"; do
    rm -rf $worker_dir # Delete old outputs so that file and directory creation times are included
    echo "=== Workers Parallel ===" >> "$output_txt"
    mpiexec -n $size python src/main_str.py ${pdfs} $worker_dir >> "$output_txt"

    rm -rf $scatter_dir # Delete old outputs so that file and directory creation times are included
    echo "=== Scatter Parallel ===" >> "$output_txt"
    mpiexec -n $size python src/main_scatter.py ${pdfs} $scatter_dir >> "$output_txt"

done

# Write results to a csv for analysis
python write2csv.py "$output_txt" "$output_csv"

echo "tests complete"
