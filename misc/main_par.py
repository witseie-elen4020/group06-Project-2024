import fitz
import os
import sqlite3
from mpi4py import MPI  # Import MPI module for parallel processing

def extract_captions(txt_file, prefix):
    """
    Extract captions from a text file based on a specified prefix.

    Args:
    - txt_file (str): Path to the text file.
    - prefix (str): Prefix indicating the type of caption (e.g., "Figure", "Table").

    Yields:
    - str: Captions extracted from the text file.
    """
    with open(txt_file, "r") as file:
        caption = []
        for line in file:
            line = line.strip()
            if line.startswith(prefix):
                caption.append(line)
            elif caption and line:  
                caption.append(line)
            elif caption and not line:  
                yield " ".join(caption)
                caption = []
        if caption:  
            yield " ".join(caption)

def find_items(pdf_file, output_dir, db_file):
    """
    Extract figures and tables captions from a PDF file and store them in a SQLite database.

    Args:
    - pdf_file (str): Path to the PDF file.
    - output_dir (str): Directory to store intermediate text files.
    - db_file (str): Path to the SQLite database file.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    comm = MPI.COMM_WORLD  # Initialize MPI communicator
    rank = comm.Get_rank()  # Get the rank of the current process
    size = comm.Get_size()  # Get the total number of processes
    
    with fitz.open(pdf_file) as doc:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS figures
                     (page INTEGER, caption TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS tables
                     (page INTEGER, caption TEXT)''')
        
        num_pages = len(doc)
        pages_per_process = num_pages // size
        start_page = rank * pages_per_process  # Calculate the starting page index for the current process
        end_page = (rank + 1) * pages_per_process if rank < size - 1 else num_pages  # Calculate the ending page index for the current process
        
        print(f"Process {rank} handling pages from {start_page} to {end_page - 1}")
        
        for page_index in range(start_page, end_page):
            page = doc[page_index]
            page_text = page.get_text()
            with open(f"{output_dir}/page_{page_index+1}.txt", "w") as txt_file:
                txt_file.write(page_text)
            figure_captions = extract_captions(f"{output_dir}/page_{page_index+1}.txt", "Figure")
            for caption in figure_captions:
                print(f"Process {rank}: Page {page_index+1}: {caption}")
                c.execute("INSERT INTO figures VALUES (?, ?)",
                          (page_index+1, caption))
            table_captions = extract_captions(f"{output_dir}/page_{page_index+1}.txt", "Table")
            for caption in table_captions:
                print(f"Process {rank}: Page {page_index+1}: {caption}")
                c.execute("INSERT INTO tables VALUES (?, ?)",
                          (page_index+1, caption))
        
        conn.commit()
        conn.close()

find_items("data/390.pdf", "pages", "data.db")
