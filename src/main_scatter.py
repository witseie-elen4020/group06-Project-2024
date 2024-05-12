# Ths script conatins and alternative apporche to parallele extraction which better leverages the features of MPI
# Instead of extrcating page data all information is sirted and stored in a set of strings.
# This allows the main thread to easilty gather ordered data and perform operations accordingly
import os

from mpi4py import MPI  # Import MPI module for parallel computing
import fitz  # Import fitz module for PDF processing
from sys import argv  # Import argv for command-line arguments

from timeit import default_timer as timer # form benchmarking
from str_job import * # holds uself contants for string-job parasing and saving


# Threadding offsets
LOG_NO = 1
TXT_NO = 2
FIG_NO = 3
TAB_NO = 4

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

def distribute_jobs(jobs, num_processes):
    # Open the PDF file and get the total number of pages
    num_jobs = len(jobs)
    
    # Calculate the number of jobs to assign to each process
    jobs_per_process = num_jobs // num_processes
    remainder = num_jobs % num_processes
    
    # Calculate start and end page for each process
    start_job = 0
    for rank in range(num_processes):
        end_job = start_job + jobs_per_process - 1
        # Distribute remaining pages evenly among the first 'remainder' processes
        if rank < remainder:
            end_job += 1
        yield (start_job, end_job)
        start_job = end_job + 1

if __name__ == "__main__":
    comm = MPI.COMM_WORLD  # Initialize MPI communicator
    rank = comm.Get_rank()  # Get the rank of the current process
    size = comm.Get_size()  # Get the total number of processes

    
    pdf_files = argv[1:-1]  # Get the path to the PDF file from command-line arguments
    output_dir = argv[-1]  # Get the path to the PDF file from command-line arguments

    if len(argv) < 3:  # Check if the correct number of command-line arguments is provided
        if rank == 0:
            print(f"Usage: {argv[0]} <pdf_files> <output_directory>")  # Print usage message from rank 0
        exit()  # Exit the program

    if rank == 0:
        print(f"Number of processes: {size}")  # Print the total number of processes from rank 0

    # Loop throuhg all pdf files provided 
    for pdf_file in pdf_files:

        _time =  MPI.Wtime() if rank == 0 else None
        # ==========
        # -- Begin extraction
        _extract_time =  MPI.Wtime() if rank == 0 else None
        # Distribute pages among processes
        page_range = list(distribute_pages(pdf_file, size))
        # _time = MPI.Wtime()-_time
        # print("Distibution time:", _time)

        # Each process opens the PDF and extracts its pages
        start_page, end_page = page_range[rank]
        extracted_text = ""  # Initialize a string to store extracted text
        contents = ""       # Holds section headdings and text, (without figure captions)
        numbers = ""        # Holds information realting to document page numbers
        jobs = ""           # Holds information realting to futher extraction jobs
        figs_str = ""       # Stores all figure captions
        tabs_str = ""       # Holds all table captions
        log = ""            # Holds a record of any error that may occure
        

        doc = fitz.open(pdf_file)
        for page_number in range(start_page, end_page + 1):
            [_txt, _cont, _numbs, _jobs, _figs_str, _tabs_str, _log] = extract_page_info(doc[page_number], page_number)
            extracted_text += _txt # Append text content of the page
            contents += _cont
            numbers += _numbs
            jobs += _jobs
            figs_str += _figs_str
            tabs_str += _tabs_str
            log += _log

        # Reduce information into main for job creation
        contents = comm.reduce(contents, root=0)
        jobs = comm.reduce(jobs, root = 0)


        if rank == 0:
            _extract_time = MPI.Wtime()- _extract_time
            

        # Now creat a set of save jobs
        _job_time =  MPI.Wtime() if rank == 0 else None
        job_pool = []
        local_jobs = []
        save_path = os.path.join(output_dir, os.path.splitext(os.path.basename(pdf_file))[0])

        
        # ==== preapre jobs
        img_save_path = os.path.join(save_path,IMG_DIR)
        if rank == 0:
            if not os.path.exists(img_save_path):
                os.makedirs(img_save_path)

            # Great a list of job strings
            # Jobs that always need to be done
            try:
                [info, content, body] = contents.split(GLOBAL_BREAK)[0:3]
                job_pool = job_pool +  [InfoJob(info, MAJOR_BREAK, MINOR_BREAK), ContentJob(content, MAJOR_BREAK, MINOR_BREAK)]
            except:
                pass
            genral_jobs = get_jobs(jobs.strip(MAJOR_BREAK).split(MAJOR_BREAK))
            job_pool += genral_jobs



        # === divide vector between processes ===

        n=0
        job_split = []
        if rank == 0:
            n = len(job_pool)
        
            div = n // size # Intager division of elements between processes ignoring remainder
            rem = n % size  # Remaining elements that cannot be evenly divided
        
            if rem != 0:
                div += 1
        
            job_split = [job_pool[i:i + div] for i in range(0, len(job_pool), div)]
            
            # Pad job slit with empy jobs if require (there are more processes than jobs)
            while len(job_split) < size:
                job_split.append(None)
        
        local_jobs = comm.scatter(job_split, root = 0)

        if not local_jobs == None:
            for job in local_jobs:
                log += job.do_job(doc, pdf_file, save_path)
        
        # Some jobs doe not warrent being sent to seperate threads as they are fast but data heavey 
        # Hance they are distributed using gather and addressed here
        # Log containing all error that have occured, in thread zero so will only be reated when all jobs are compted
        log_save_rank = LOG_NO%size
        log = comm.gather(log, root = log_save_rank)
        if rank == log_save_rank:
            with open(os.path.join(save_path, "log.txt"), "w") as file:
                file.write("".join(log))

        # Save a list of all figure found 
        img_save_rank = FIG_NO%size
        figs_str = comm.reduce(figs_str, root=img_save_rank)
        if rank == img_save_rank:
            with open(os.path.join(save_path, IMG_FILE), "w") as file:
                file.write(figs_str)

        tab_save_rank = TAB_NO%size
        tabs_str = comm.reduce(tabs_str, root=tab_save_rank)
        if rank == tab_save_rank:
            with open(os.path.join(save_path, TAB_FILE), "w") as file:
                file.write(tabs_str)

        txt_save_rank = TXT_NO%size
        extracted_text = comm.reduce(extracted_text, root=txt_save_rank)
        if rank == txt_save_rank:
            with open(os.path.join(save_path, TEXT_FILE), "w") as file:
                file.write(extracted_text)


        comm.barrier()
        if rank == 0:
            _job_time = MPI.Wtime()-_job_time
            _time = MPI.Wtime()-_time
            print("---------------------------")
            print(f"File: {pdf_file}")
            print(f"Pages: {len(doc)}")
            print(f"Jobs: {n}")
            print(f"Extraction Time: {_extract_time}")
            print(f"Job Time: {_job_time}")
            print(f"Total Time: {_time}")

    if rank == 0:
        print("---------------------------\n")

