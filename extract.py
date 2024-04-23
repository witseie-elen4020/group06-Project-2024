# This Script contains a simple console interface to test the efectivenss of data extraction tools
from sys import argv

from pdfExtractor import find_items
from extract_page import *

# ===================================
# General constants 

DB_FILE = "data.db"
LOG_FILE = "Logs.txt"
FIG_DIR = "Figures"
TEXT_DIR = "Text"



# ===================================

def print_help():
    print("TODO: make help instructions")

if __name__ == "__main__":

    if len(argv) == 1:
        print(f"Usage: {argv[0]} <list-of-input-pdfs>")
    input_files = argv[1:]

  

    for in_file in input_files:
        print(in_file)
        #find_items(in_file, FIG_DIR, DB_FILE)
        extract_from_doc(in_file)

    # # loop through input arguments 

    # skip_flag = False # Set to true if next argument should be skipped
    # help_falg = False # set to true is help infimation should be displayed (without running code)
    # for i in range(1, len(argv)):
    #     if skip_flag:
    #         skip_flag =False
    #     elif argv[i] == "-h" or argv[i] == "--help":
    #         help_falg = True
    #         print_help()
    #     elif argv[i] == "-f"
            
            
