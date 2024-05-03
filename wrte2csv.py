# A simple script used to help recod benchmark times for pdf extraction
from sys import argv
import csv
def extract_results(infile:str, outfile:str):
    with open(infile, 'r') as f:
        lines = f.readlines()
        rows = [["Method", "Processes", "File", "Pages", "Jobs", "Extract_Time", "Job_Time", "Total_Time"]]
        method = "None"
        processes = 0
        row = []
        for line_no, line in enumerate(lines):
            if line.startswith("=== "):
                method = line.split()[1]
            elif line.startswith("Number of processes:"):
                processes = line.split()[3]
            elif line.startswith("File:") or line.startswith("Pages:") or line.startswith("Job") or line.startswith("Extraction") or line.startswith("Total"):
                row.append(line.split()[-1])
                if line.startswith("Total"):
                    rows.append([method, processes] + row)
                    row = []
        f.close()

    with open(outfile,'w') as o:
        writer = csv.writer(o)
        writer.writerows(rows)
        o.close()


if __name__ == "__main__":
    if len(argv) == 3:
        extract_results(argv[1], argv[2])
    else:
        print(f"Usage: {argv[0]} <input-file> <output-file>")
