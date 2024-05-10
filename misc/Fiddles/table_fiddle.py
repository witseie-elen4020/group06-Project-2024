# This script is used to specifcally test table extraction
#
# Helpful link: https://medium.com/@pymupdf/table-recognition-and-extraction-with-pymupdf-54e54b40b760
# Official docs: https://pymupdf.readthedocs.io/en/latest/page.html#Page.find_tables
import fitz
import csv
import os
from sys import argv

SUCCESS_STR = "--- success ---"
WARN_STR = "!-- Warning --!"


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
                # Check was too strict and missed tables: try a more lenient approach
                tabs = page.find_tables(strategy="lines_strict")
                print(f"was too easy but now {capt_count} vs {len(tabs.tables)}")
            else:   # There are more tables than caption, test was too lineient
                tabs = page.find_tables(strategy="text", min_words_vertical = 10, min_words_horizontal = 10)
                print(f"was too strict but now {capt_count} vs {len(tabs.tables)}")
            
            # Now extract tables
            for i,tab in enumerate(tabs):
                
                rows = tab.extract()
                tab_name = "Tab_" + tab_captions[i].split()[1]
                outfile = os.path.join(OUT_DIR, tab_name)+".csv"
                with open(outfile,'w') as o:
                    for row_nuumb,row in enumerate(rows):
                        try:
                            writer = csv.writer(o)
                            writer.writerow(row)
                        except UnicodeEncodeError as e:
                            print("gg")
                            print(e.args)
                            print(len(row))
                    o.close()
                        
# Recursive funtion used to find tables in the docuemnt
def get_tabs(tab_capts, page: fitz.Page, logs =[], stratergy="lines_strict"):
    #Storres andy issues wich may occures
    # First use strick lines to see if tables are found (this tends to be most accurate)
    tabs = page.find_tables(strategy="lines")
    tab_count = len(tabs.tables)
    capt_count = len(tab_capts)
    if tab_count == capt_count:
        # Inital table idenfication deemed successful
        logs.append(SUCCESS_STR)
        logs.append(f"{capt_count} found as expected")
        return tabs, logs
    elif tab_count > capt_count:
        # More tables have been found than there are captions availabe
        # Use more stringent table idenifcation
        tabs = page.find_tables(strategy="lines_strict")
        tab_count = len(tabs.tables)
        logs.append(f"{tab_count} tables found with only {capt_count} expected")
    else:
        # Table finding was too strict, try using plane text
        tabs = page.find_tables(strategy="text")
        tab_count = len(tabs.tables)


if __name__ == "__main__":
    files = argv[1:]
    for file in files:
        extract_tabs(file)



