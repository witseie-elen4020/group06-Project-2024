#!/usr/bin/env bash
arr=()
for pdf_file in $1/*.pdf; do
    arr+=" "
    arr+=$pdf_file
done

python extract_serial.py ${arr}