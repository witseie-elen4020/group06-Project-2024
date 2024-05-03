# An Example of the full serial system, including genral page infroation aqauestion  

import fitz
from fitz import Rect
import os
import io
from typing import Tuple,List
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from mpi4py import MPI
from timeit import default_timer as timer # form benchmarking
from sys import argv

from extract_error import ExtractionError

# ===================================
# General constants 

DB_FILE = "data.db"
LOG_FILE = "Logs.txt"
FIG_DIR = "Figures"
TEXT_FILE = "Text.txt"

OUT_DIR = "Data"


# Values to be leverged on when using Geo documents 

# Page dimations for A4
X_MAX = 595
Y_MAX = 842

TITLE_RECT = Rect(180, 450, X_MAX, 520)     # Genral postiton of document tilte on conver page
AUTHOR_RECT = Rect(180, 535, X_MAX, 620)    # Ganral postion of author names on cover page

TITLE_RECT1 = Rect(180, 450, X_MAX, 520)    # Genral postiton of document tilte on second page
DATE_RECT = Rect(0, 755, X_MAX, 7765)       # Ganral postion of date on second page

ABSTRACT_START_TXT = "ABSTRACT"
CONTENT_START_TXT = "CONTENTS "
PAGE_TXT = "Page"
END_TXT = "_oOo_"

# ===================================

# Info extraction setup
# This is used to get genral page inforamtion like title, author and sections
# The scope for parellisation is limited becuase abstract and table of content may run over multiple pages

# This function take in the conver page of EGRI document and exploits the layout to retrun tilte and author information
# It is assumed that any document sent to this function is verified as having come from EGRI and will thus follow their genral formats
# Outputs: Tilte (string), authors (string)
def get_page0_info(page:fitz.Page)->Tuple[str, str]:

    # Use text page for more effecient extraction
    textpage = page.get_textpage()

    # Attempt to find title info
    title_txt = page.get_textbox(TITLE_RECT, textpage=textpage)
    title_txt = ' '.join(title_txt.split())

    # Attempt to find authors
    authors_txt = page.get_textbox(AUTHOR_RECT, textpage=textpage)
    authors_txt = authors_txt.strip()
    authors_txt = " ".join(authors_txt.replace("\n", ",").replace(" AND", ",").split()).replace(",,",",").replace(", ,",",") # Ensure that list of authors is seperated by commas only

    return title_txt, authors_txt

# Extracts usful inforation from page 1 (second page of pdf) of EGRI docuemnted, including full text
# Returns the data and genral text extracted from the doucment
def get_page1_info(page:fitz.Page)->Tuple[str, str]:
    textpage = page.get_textpage()
    txt = page.get_text("text", textpage=textpage)
    date_txt = txt.strip().rsplit("\n", 1)[-1] # Find and publication date at end of text
    return date_txt, txt

# Find the document abstrct from page 2-3 (zero indexed) and content from page 3-6
# Returns abstract text and table of content dictionary - excess or an error message if no abstract is found
# Throws and `ExtractionError` if no abstract can be found on the given page
# === WIP: hard to accuratly parallise due to finge cases where abstract and table of contents span over multipe pages
def get_abstract_and_contents(doc:fitz.Document, start_pt = 2):

    abstract_pgs = 1 # Stores the number of pages used by abstract and contents section
    content_pgs = 1 # Number of pages used by table of content

    # First page in list should contain abstract
    textpage0 = doc[2].get_textpage()
    textpage1 = doc[3].get_textpage()

    # === Abtract ===
    abstract_txt = "Not found."
   
    # Use these two rects to locate the baounding box of the abstrct
    abstract_start = doc[start_pt].search_for(ABSTRACT_START_TXT, textpage=textpage0) # Directly above abstrct
    # Chack that abstract start was found
    if(len(abstract_start) == 0 or len(abstract_end) == 0):
        raise ExtractionError("Abstract start could not be found", 2)
    
    # Find abstract end box: this may span over two pages
    abstract_end = doc[0].search_for(END_TXT, textpage=textpage0)             
    # Chack that abstract end was found, set to two pages if not
    if(len(abstract_end) == 0):
        # Abstract spans two pages
        abstract_end = doc[1].search_for(END_TXT, textpage=textpage1)  
        abstract_pgs = 2

        # It assumed that an abstract will span a maximum of two pages
        if(len(abstract_end) == 0):
            raise ExtractionError("Abstract end could not be found", 3)
        
        # Extrat abstaxt over two pages
        abstract_rect0 = Rect(0, abstract_start[0][3], X_MAX, Y_MAX)
        abstract_rect1 = Rect(0, 0, X_MAX, abstract_end[0][1])

        abstract_txt = doc[2].get_textbox(abstract_rect0).strip()+doc[3].get_textbox(abstract_rect1).strip()
    else:
        # Extrat apstract from page based on the rect location determined
        abstract_rect = Rect(0, abstract_start[0][3], X_MAX, abstract_end[0][1])
        abstract_txt = doc[2].get_textbox(abstract_rect).strip()


    # === Table of contents...

    return abstract_txt

# Function used to extract table of contents fro the fourth page of a document
def get_page3_info(page:fitz.Page):
    return

if __name__ == "__main__":
    if len(argv) == 1:
        print(f"Usage {argv[0]} <filenames>")
        exit()
    file = argv[1]
