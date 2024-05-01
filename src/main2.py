from mpi4py import MPI  # Import MPI module for parallel computing
import fitz  # Import fitz module for PDF processing
from sys import argv  # Import argv for command-line arguments
from page_data import PageData  # Import the PageData class 

from timeit import default_timer as timer # form benchmarking

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
    comm = MPI.COMM_WORLD  # Initialize MPI communicator
    rank = comm.Get_rank()  # Get the rank of the current process
    size = comm.Get_size()  # Get the total number of processes

    if len(argv) != 3:  # Check if the correct number of command-line arguments is provided
        if rank == 0:
            print(f"Usage: {argv[0]} <pdf_file> <output_txt>")  # Print usage message from rank 0
        exit()  # Exit the program

    pdf_file = argv[1]  # Get the path to the PDF file from command-line arguments
    output_txt = argv[2]  # Get the path to the PDF file from command-line arguments

    if rank == 0:
        print(f"Number of processes: {size}")  # Print the total number of processes from rank 0
    # Distribute pages among processes

    pool = [1,2,3,4,5,6,7,8] if rank == 0 else None
    busy = True
    has_job = False
    job_id = -1
    worker_rank = rank

    # if busy:
    #     if rank != 0:
    #         # Send job reqest
    #         worker_rank = rank
    #         comm.send(worker_rank,0,1)
    #         job_id = comm.recv(job_id, 0, 2)
    #         print("Got job")

    #     else:
    #         #worker_rank = comm.Recv(worker_rank, tag=1)
    #         print(f"request from workker {worker_rank}")
    #         pool.pop()
    #         if len(pool) == 0:
    #             busy = False
        
    #     if busy==False:
    #         comm.bcast(busy, 0)



    _time = MPI.Wtime()
    page_range = list(distribute_pages(pdf_file, size))
    _time = MPI.Wtime()-_time
    print("Distibution time:", _time)

    # Each process opens the PDF and extracts its pages
    _time = MPI.Wtime()
    start_page, end_page = page_range[rank]
    extracted_text = ""  # Initialize a string to store extracted text
    page_datas = []
    for page_number in range(start_page, end_page + 1):
        with fitz.open(pdf_file) as doc:
            page_data = PageData(doc[page_number], page_number)
            page_datas.append(page_data)
            extracted_text += page_data.raw_txt  # Append text content of the page
    _time = MPI.Wtime()-_time
    print("Extraction Time:", _time)

    # # # pd = {}
    
    _time = MPI.Wtime()
    # Send page datas to main threa
    if rank != 0:
        print("Im gonna do a thing", rank)
        comm.send(page_datas,0,tag=1)

    if rank==0:
        for _ in range(1,size):
            data = comm.recv()
            page_datas.append(data)

        _time = MPI.Wtime()-_time
        print("Send Time:", _time)


    _time = MPI.Wtime()
    # Gather extracted text from all processes
    all_extracted_text = comm.gather(extracted_text, root=0)
    _time = MPI.Wtime()-_time
    print("Gather Time:", _time, "for rank ", rank)
    if rank == 0:
        
        _time = timer()
        # Write the gathered text to the output file
        with open(output_txt, 'w') as f:
            for text in all_extracted_text:
                f.write(text)
        _time = timer()-_time
        print(_time)