#!/usr/bin/env bash
arr=()
for pdf_file in $1/*.pdf; do
    arr+=" "
    arr+=$pdf_file
done

python initial_results/extract_serial.py ${arr} >> initial_results/results.txt

# Write results to a csv
python initial_results/get_results.py initial_results/results.txt initial_results/results.csv