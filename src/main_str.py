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
import str_job
from doc_data import DocData


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

def extract_page_info(page:fitz.Page, page_index:int):

    raw_txt = ""        # Holds all text from page (including figure captions)
    contents = ""       # Holds section headdings and text, (without figure captions)
    numbers = ""        # Holds information realting to document page numbers
    jobs = ""           # Holds information realting to futher extraction jobs
    log = ""            # Holds a record of any error that may occure

    run_on_job = ""        # Holds a job which may be split over multiple pages

    fig_capts = []     # Holds figure caption
    doc_pg_no = 0

    # Flags
    roj_end = False # run on job ends on this page
    roj_start = False # run on job start on this page
    hide_flag = False # Content should not be written to a section

    textpage = page.get_textpage()  # Use a textpage for faster text extraction 
    txt = textpage.extractText(sort=True)
    # Find chunck instead of blocks becuase this has more reliable whitesapce behavior
    chunks = txt.replace("\n ","\n").split("\n\n")
    for i,chunk in enumerate(chunks):
        chunk = ' '.join(chunk.split()).strip() # Clean chunck
        if chunk.isupper(): # Indcative of a headding
            contents += MAJOR_BREAK + chunk + MINOR_BREAK # Add section start to headding
            hide_flag = True
        elif chunk.startswith(FIG_TXT): # Whole Chunk will be the figure caption
            fig_capts.append(chunk)
            hide_flag = True
        elif chunk.startswith(TAB_TXT) and 1==2: # Whole chunk will be table cpation
            assert(False)
        elif END_TXT in chunk:
            contents = contents + GLOBAL_BREAK
            hide_flag = True
        if chunk != "":
            raw_txt += chunk + '\n'
            if page_index <= MAX_CONTENT and not hide_flag:
                contents += chunk + '\n'
        # Reset hide flag to false
        hide_flag = False
        
    # Find printed page number (if present)
    try:
        [tmp, pg_no] = raw_txt.strip().rsplit('\n',1)
        doc_pg_no = int(pg_no)
        numbers = f"--- PDF {page_index+1} DOC {doc_pg_no} ---"
        raw_txt = f"\n{numbers}\n" + tmp
    except:
        numbers = f"--- PDF {page_index+1} DOC 0 ---"
        raw_txt = f"\n{numbers}\n" + raw_txt
        

    # Find images to be extracted and creat correspoding jobs

    try:
        # Get figure xrefs for extraction
        img_xrefs = page.get_images()

        capt_count = len(fig_capts)
        xref_count = len(img_xrefs)
    
        if capt_count != xref_count: # Chack to see if all images were found
            if capt_count == 0:
                raise ExtractionNote(f"Ignored {xref_count} uncaptioned images", page_index)
            elif capt_count == 1:
                raise ExtractionError(f"Could not find image with caption: '{fig_capts[0][:20]}...' ", page_index)
            
            # More than one figure, detemine which images are captioned
            good_xrefs = []
            good_capts = []
            # The bounding boxes of all page captions 
            capt_bbs = [page.search_for(capt, textpage=textpage)[0] for capt in fig_capts]
            for capt_i, bb in enumerate (capt_bbs):
                
                # Bounds of figure location
                ymin = 0 if capt_i == 0 else capt_bbs[capt_i-1][3]
                ymax = bb[1]

                _capt_images = [xref for xref in img_xrefs if (xref[2] > ymin and xref[2] < ymax)]

                if(len(_capt_images) == 0):
                    log += str(ExtractionError(f"Could not find image with caption: '{fig_capts[capt_i][:20]}...' ", page_index))+'\n'
                    continue
                elif(len(_capt_images) > 1):
                    log += str(ExtractionNote(f"Ignored {len(_capt_images -1 )} uncaptioned images above figure caption {fig_capts[capt_i][:20]}...'", page_index))+'\n'
                
                # Assume valid image to be the lowest one
                good_capts.append(fig_capts[capt_i])
                good_xrefs.append(_capt_images[-1])
            
            # Set captions and xrefs to good ones
            fig_capts = good_capts
            img_xrefs = good_xrefs
            
        # Now make image jobs
        assert(len(fig_capts) == len(img_xrefs))

        for capt_i, capt in enumerate(fig_capts):
            jobs += str_job.get_img_job_str(capt, img_xrefs[capt_i][0], str(page_index), str(doc_pg_no)) + MAJOR_BREAK
                
    except ExtractionError as e:
        log += str(e) + '\n'
    except ExtractionNote as e:
        log += str(e) + '\n'
     
    return raw_txt, contents, numbers, jobs, log  
if __name__ == "__main__":
    comm = MPI.COMM_WORLD  # Initialize MPI communicator
    rank = comm.Get_rank()  # Get the rank of the current process
    size = comm.Get_size()  # Get the total number of processes

    if len(argv) != 3:  # Check if the correct number of command-line arguments is provided
        if rank == 0:
            print(f"Usage: {argv[0]} <pdf_file> <output_txt>")  # Print usage message from rank 0
        exit()  # Exit the program

    pdf_file = argv[1]  # Get the path to the PDF file from command-line arguments
    output_dir = argv[2]  # Get the path to the PDF file from command-line arguments

    if rank == 0:
        print(f"Number of processes: {size}")  # Print the total number of processes from rank 0

    _time =  MPI.Wtime() if rank == 0 else None
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
    log = ""            # Holds a record of any error that may occure
    

    doc = fitz.open(pdf_file)
    for page_number in range(start_page, end_page + 1):
        [_txt, _cont, _numbs, _jobs, _log] = extract_page_info(doc[page_number], page_number)
        extracted_text += _txt # Append text content of the page
        contents += _cont
        numbers += _numbs
        jobs += _jobs
        log += _log
    
    if rank == 0:
        _time = MPI.Wtime()-_time
        print("Extraction Time:", _time)

    _time =  MPI.Wtime() if rank == 0 else None
    # Gather extracted text from all processes
    extracted_text = comm.gather(extracted_text, root=0)
    contents = comm.gather(contents, root=0)
    numbers = comm.gather(numbers, root=0)
    jobs = comm.gather(jobs, root=0)
    log = comm.gather(log)

    if rank == 0:
        _time = MPI.Wtime()-_time
        print("Gather Time:", _time)

    # Now creat a set of save jobs
    save_jobs = []
    save_path = os.path.join(output_dir, pdf_file)
    if rank == 0:
        # Make save folders
        img_save_path = os.path.join(save_path,str_job.IMG_DIR)
        if not os.path.exists(img_save_path):
            os.makedirs(img_save_path)

        # There is no benefit in doing text in a seperatre job, it is too large to send and faster to do here
        with open(os.path.join(save_path, str_job.TEXT_FILE), "w") as file:
            file.write("".join(extracted_text))

        # Great a list of job strings
        # Jobs that always need to be done
        job_pool = []
        try:
            [info, content, body] = "".join(contents).split(GLOBAL_BREAK)[0:3]
            job_pool = job_pool +  [str_job.InfoJob(info, MAJOR_BREAK, MINOR_BREAK), str_job.ContentJob(content, MAJOR_BREAK, MINOR_BREAK)]
        except:
            pass
        genral_jobs = str_job.get_jobs("".join(jobs).strip(MAJOR_BREAK).split(MAJOR_BREAK))
        job_pool += genral_jobs

    
    # Asycn manager worker system
    _time = MPI.Wtime()
    busy = True
    if rank == 0:
        log = "".join(log)
        pool_len = len(job_pool)
        for __ in range(pool_len+size-1):
            req = comm.irecv(tag=JOB_REQUEST)
            worker_rank = req.wait()
            job = job_pool.pop() if len(job_pool) > 0 else None
            req = comm.isend(job, dest=worker_rank, tag=JOB_DISPATCH)
        busy = False
        _time = MPI.Wtime()-_time
        print("Job Time:", _time)
    else:
        log = ""
        while busy:
            # Request a job from manager thread
            req = comm.isend(rank, dest=0, tag=JOB_REQUEST)
            # Recive job request
            job_req = comm.irecv(source=0, tag=JOB_DISPATCH)
            job = job_req.wait()
            if job == None:
                busy = False
                break
            else:
                log += job.do_job(doc, pdf_file, save_path)

    log = comm.gather(log, root = 0)
    if rank == 0:
        with open(os.path.join(save_path, "log.txt"), "w") as file:
            file.write("".join(log))
