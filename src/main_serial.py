# Ths script conatins and alternative apporche to parallele extraction which better leverages the features of MPI
# Instead of extrcating page data all information is sirted and stored in a set of strings.
# This allows the main thread to easilty gather ordered data and perform operations accordingly
import os

from mpi4py import MPI  # Import MPI module for parallel computing
import fitz  # Import fitz module for PDF processing
from fitz import Rect
from sys import argv  # Import argv for command-line arguments
from page_data import PageData  # Import the PageData class 

from timeit import default_timer as timer # form benchmarking
from extract_error import ExtractionError, ExtractionNote
from str_job import *


# ====================
# --- Constants ---

# -- For text fromatting --
GLOBAL_BREAK = ">>x<<"
MAJOR_BREAK = "]==["
MINOR_BREAK = ")--("

# -- For writng styles ---
# Captions 
FIG_TXT = "Figure"
TAB_TXT = "Table"

# genral structure
EXPECTED_ABSTRACT = 2
MAX_ABSTRACT = 3
EXPECTED_CONTENT = 3
MAX_CONTENT = 4

# Key words to look for 
ABSTRACT_START_TXT = "ABSTRACT"
CONTENT_START_TXT = "CONTENTS "
PAGE_TXT = "Page"
END_TXT = "_oOo_"

# Page dimations for A4
X_MAX = 595
Y_MAX = 842

# Communication tags
JOB_REQUEST = 11
JOB_DISPATCH = 22

# ================

# Function to distribute pages evenly across processes
def distribute_pages(pdf_file, num_processes):
    # Open the PDF file and get the total number of pages
    num_pages = len(fitz.open(pdf_file))
    
    # Calculate the number of pages to assign to each process
    pages_per_process = num_pages // num_processes
    remainder = num_pages % num_processes
    
    # Calculate start and end page for each process
    start_page = 0
    for rank in range(num_processes):
        end_page = start_page + pages_per_process - 1
        # Distribute remaining pages evenly among the first 'remainder' processes
        if rank < remainder:
            end_page += 1
        yield (start_page, end_page)
        start_page = end_page + 1


if __name__ == "__main__":

    if len(argv) < 3: 
        print(f"Usage: {argv[0]} <pdf_file> <output_txt>")  # Print usage message from rank 0
        exit()  # Exit the program

    pdf_files = argv[1:-1]  # Get the path to the PDF file from command-line arguments
    output_dir = argv[-1]  # Get the path to the PDF file from command-line arguments

    print(f"Number of processes: 1 (Serial)")  # Print the total number of processes from rank 0

    # Loop throuhg all pdf files provided 
    for pdf_file in pdf_files:

        _time =  timer()
        # ==========
        # -- Begin extraction
        _extract_time =  timer()

        # Each process opens the PDF and extracts its pages
        extracted_text = ""  # Initialize a string to store extracted text
        contents = ""       # Holds section headdings and text, (without figure captions)
        numbers = ""        # Holds information realting to document page numbers
        jobs = ""           # Holds information realting to futher extraction jobs
        figs_str = ""       # Stores all figure captions
        tabs_str = ""
        log = ""            # Holds a record of any error that may occure
        

        doc = fitz.open(pdf_file)
        for page_number,page in enumerate(doc):
            [_txt, _cont, _numbs, _jobs, _figs_str, _tabs_str, _log] = extract_page_info(page, page_number)
            extracted_text += _txt # Append text content of the page
            contents += _cont
            numbers += _numbs
            jobs += _jobs
            figs_str += _figs_str
            tabs_str += _tabs_str
            log += _log


        _extract_time = timer()- _extract_time

        # Now creat a set of save jobs
        _job_time =  timer()
        save_jobs = []
        save_path = os.path.join(output_dir, os.path.splitext(os.path.basename(pdf_file))[0])
        
        # Make save folders
        img_save_path = os.path.join(save_path,IMG_DIR)
        if not os.path.exists(img_save_path):
            os.makedirs(img_save_path)

        # Great a list of job strings
        # Jobs that always need to be done
        job_pool = []
        try:
            [info, content, body] = "".join(contents).split(GLOBAL_BREAK)[0:3]
            job_pool = job_pool +  [InfoJob(info, MAJOR_BREAK, MINOR_BREAK), ContentJob(content, MAJOR_BREAK, MINOR_BREAK)]
        except:
            pass
        genral_jobs = get_jobs("".join(jobs).strip(MAJOR_BREAK).split(MAJOR_BREAK))
        job_pool += genral_jobs

        for job in job_pool:
            log += job.do_job(doc, pdf_file, save_path)
            

        # Log containing all error that have occured
        with open(os.path.join(save_path, "log.txt"), "w") as file:
            file.write("".join(log))

        # Save a list of all figure found 
        capts = "".join(figs_str)
        with open(os.path.join(save_path, IMG_FILE), "w") as file:
            file.write(capts)
            
        # There is no benefit in doing text in a seperatre job
        with open(os.path.join(save_path, TEXT_FILE), "w") as file:
            file.write("".join(extracted_text))

        with open(os.path.join(save_path, TAB_FILE), "w") as file:
            file.write(tabs_str)

        _job_time = timer()-_job_time
        _time = timer()-_time
        print("---------------------------")
        print(f"File: {pdf_file}")
        print(f"Pages: {len(doc)}")
        print(f"Jobs: {len(job_pool)}")
        print(f"Extraction Time: {_extract_time}")
        print(f"Job Time: {_job_time}")
        print(f"Total Time: {_time}")
    print("---------------------------")

