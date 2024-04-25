# Used to extract inital benchmark results for parallel image reading from a text files
import os
import csv
import sys

def extract_results(infile:str, outfile:str):
    with open(infile, 'r') as f:
        lines = f.readlines()
        rows = [["Page", "Image Time", "Image Count", "Text Time", "Characters", "Caption Time", "Caption Count", "Save Time", "Save Count"]]

        for line_no, line in enumerate(lines):
            if line.startswith("---"):
                row = [line.split()[-1]] # Get page number
                row = row + 8*[0.0] # Array of flotas to store times
                for _i in range(0,4):
                    #row[_i] = int(lines[line_no+_i][2])
                    line_vals = lines[line_no+_i+1].split()
                    row[2*_i+1] = line_vals[2]  # This column corresponds to the time taken
                    row[2*_i+2] = line_vals[-2] #this colum  corresponds to the number of items
                rows.append(row)
        f.close()

    with open(outfile,'w') as o:
        writer = csv.writer(o)
        writer.writerows(rows)
        o.close()


if __name__ == "__main__":
    if len(sys.argv) == 3:
        extract_results(sys.argv[1], sys.argv[2])
    else:
        INFILE = "results.txt"
        OUTFILE = "results.csv"
        extract_results(INFILE, OUTFILE)

    

    