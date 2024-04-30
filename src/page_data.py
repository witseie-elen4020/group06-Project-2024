# Contains class definetions which can aid in page 
import fitz
from fitz import Rect
import os
import io
from sys import argv
from typing import Tuple,List

from extract_error import ExtractionError

# =========================
# Sections
# Key words to look for 
ABSTRACT_START_TXT = "ABSTRACT"
CONTENT_START_TXT = "CONTENTS "
PAGE_TXT = "Page"
END_TXT = "_oOo_"

# Captions 
FIG_TXT = "Figure"
TAB_TXT = "Table"

# genral structure
EXPECTED_ABSTRACT = 2
MAX_ABSTRACT = 3
EXPECTED_CONTENT = 3
MAX_CONTENT = 4

# =========================

# Contains useful infroation for a given page wich can help streamline the data-saving porcess
class PageData():
    def __init__(self, page:fitz.Page, page_index:int) -> None:

        # Get textpage for faster data extraction
        self.textpage = page.get_textpage()
        self.page_index = page_index

        # initalis variables
        self.raw_txt = ""       # Text contined on page: to be printed
        self.fig_capts = []     # Holds figure caption
        self.table_capts = []   # Holds table captions
        self.headding = []      # Holds CAPLTALISED section headdings that occure on the page
        self.doc_page_numer = -1    # Holds the page number as printed PDF
        self.img_xrefs = page.get_images()  # Holds refferances to all imageson the page
        self.abstract_start = False # Set to true iff the abstract starts in this page
        self.content_start = False  # Set to true iff table of content starts on page
        self.is_end = False         # Set to true iff page is the end of a section denonted by _oOo_ 

        txt = self.textpage.extractText(sort=True)
        # Find chunck instead of blocks becuase this has more reliable whitesapce behavior
        chunks = txt.replace("\n ","\n").split("\n\n")
        self.raw_txt = ""
        for chunk in chunks:
            chunk = ' '.join(chunk.split()).strip()
            if chunk == ABSTRACT_START_TXT:
                # Page contains the start of the abstract, flag accordingly
                self.abstract_start = True
                self.title = self.raw_txt
                self.raw_txt = "" # This page need only contain the abstract
            elif chunk == END_TXT:
                self.is_end = True
                self.completed = self.abstract_start
            if chunk.startswith(FIG_TXT): # Whole Chunk will be the figure caption
                self.fig_capts.append(chunk)
                continue
            elif chunk.startswith(TAB_TXT): # Whole chunk will be table cpation
                self.table_capts.append(chunk)
            if(not chunk.isspace()):
                self.raw_txt += chunk + '\n'
        
        # Find printed page number (if present)
        [tmp, pg_no] = self.raw_txt.strip().rsplit('\n',1)
        if pg_no.isnumeric():
            self.doc_page_numer == int(pg_no)
            self.raw_txt = f"--- PDF {page_index+1} DOC {pg_no} ---\n" + tmp
        else:
            self.raw_txt = f"--- PDF {page_index+1} DOC ___ ---\n" + tmp
            

        
# Used for testing
if __name__ == "__main__":
    if len(argv) == 2:
        print(f"Usage {argv[0]} <filename> <page-number")
        exit()
    file = argv[1]
    page_no = int(argv[2])

    with fitz.open(file) as doc:
        data = PageData(doc[page_no], page_no)
        print(data.raw_txt)
        print(f"Images:\n{data.fig_capts}")
        print(f"image xrefs: {len(data.img_xrefs)}")

