# this script contains a parellised verion of page extraction porotocall using multithredding
import fitz
import os
import io
from PIL import Image
from PIL.PngImagePlugin import PngInfo

from mpi4py import MPI

# ===================================
# General constants 

DB_FILE = "data.db"
LOG_FILE = "Logs.txt"
FIG_DIR = "Figures"
TEXT_DIR = "Text"

OUT_DIR = "Data"

# ===================================

# performs parellised data extraction
def extract_parallel(filename):
    # Create mpi com world
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    # Opend the doucment in process zero
    doc = fitz.open(filename) if rank == 0 else None
    local_doc =[]

    # determine how doc will be divided between porcesses
    if rank == 0:
        _n = len(doc)
        div = _n // size # Intager division of pages between processes ignoring remainder
        rem = _n % size  # Remaining elements that cannot be evenly divided
        
        # Costruct an arry of split sizes for scatterv
        split_sizes = [div+1] * rem + [div] * (size-rem) # First few elements need to be larger to account for uneven distribution
        split_displacments = [0] * size # no addtional displacments required
        for i in range(1,size):
            split_displacments[i] = split_displacments[i-1] + split_sizes[i-1] 

        print(doc)

    # scatter pages between porcesses
    comm.Scatterv([doc,split_sizes, split_displacments, fitz.Page], local_doc, root=0)

            


    
# ================================
# test code - not for genral feature use
if __name__ == "__main__":
    extract_parallel("data/390.pdf")
