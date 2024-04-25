# This script is used to specifcally test table extraction
#
# Helpful link: https://medium.com/@pymupdf/table-recognition-and-extraction-with-pymupdf-54e54b40b760
# Official docs: https://pymupdf.readthedocs.io/en/latest/page.html#Page.find_tables
import fitz
import csv
import os
from sys import argv

OUT_DIR = "Data"

def extract_tabs(file:str):
    with fitz.open(file) as pdf_file:

        if not os.path.exists(OUT_DIR):
            os.makedirs(OUT_DIR)
        for numb, page in enumerate(pdf_file): 

            print(f"=== Page {numb} =========================================")
            # Find hable headdings
            lines = page.get_text().split("\n")
            tab_captions = []
            for line in lines:
                if line.startswith("Table"):
                    print(line, "... was found\n")
                    tab_captions.append(line)

            tabs = page.find_tables(strategy="lines")
            #print(f"{len(tabs.tables)} tables were found")

            capt_count = len(tab_captions)
            tab_count = len(tabs.tables)
            if capt_count == tab_count:
                print(" -- Success ---")
            elif capt_count < tab_count:
                # Chack was too strict and missed tables: try a more linient approach
                tabs = page.find_tables(strategy="lines_strict")
                print(f"was too easy but now now {capt_count} vs {len(tabs.tables)}")
            else:   # There are more tables than caption, test was too lineient
                tabs = page.find_tables(strategy="text", min_words_vertical = 10, min_words_horizontal = 10)
                print(f"was too strict but now {capt_count} vs {len(tabs.tables)}")
            
            # Now extract tables
            for i,tab in enumerate(tabs):
                
                rows = tab.extract()
                tab_name = "Tab_" + tab_captions[i].split()[1]
                outfile = os.path.join(OUT_DIR, tab_name)+".csv"
                with open(outfile,'w') as o:
                    writer = csv.writer(o)
                    writer.writerows(rows)
                    o.close()


if __name__ == "__main__":
    files = argv[1:]
    for file in files:
        extract_tabs(file)



