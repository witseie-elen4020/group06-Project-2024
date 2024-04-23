# this script contains a parellised verion of page extraction porotocall using multithredding

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
def extract_parallel(file_list):
    # Create mpi com world
    comm = MPI.COMM_WORLD
    size = comm.size()
    rank = comm.rank()
