# Contains class definetions which can aid in page 
import fitz
from fitz import Rect
import os
import io
from sys import argv
from typing import Tuple,List

from timeit import default_timer as timer # form benchmarking

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
        textpage = page.get_textpage()
        self.page_index = page_index

        # initalis variables
        self.raw_txt = ""       # Text contined on page: to be printed
        self.fig_capts = []     # Holds figure caption
        self.table_capts = []   # Holds table captions
        self.headdings = []     # Holds CAPLTALISED section headdings that occure on the page
        self.sections = []      # Holds text blocks split up into sections 
        self.doc_page_numer = -1    # Holds the page number as printed PDF
        self.img_xrefs = page.get_images()  # Holds refferances to all imageson the page
        self.abstract_start = False # Set to true iff the abstract starts in this page
        self.content_start = False  # Set to true iff table of content starts on page
        self.is_end = False         # Set to true iff page is the end of a section denonted by _oOo_ 
        self.logs = []              # Contains a list of log lessages


        
        self.pre_fig = []  # Useful for finding correct drawing to correspond to caption

        txt = textpage.extractText(sort=True)
        # Find chunck instead of blocks becuase this has more reliable whitesapce behavior
        chunks = txt.replace("\n ","\n").split("\n\n")
        self.raw_txt = ""
        for i,chunk in enumerate(chunks):
            chunk = ' '.join(chunk.split()).strip()
            if chunk == ABSTRACT_START_TXT:
                # Page contains the start of the abstract, flag accordingly
                self.abstract_start = True
                self.title = self.raw_txt
                self.raw_txt = "" # This page need only contain the abstract
            elif chunk == END_TXT:
                self.is_end = True
                self.completed = self.abstract_start
            elif chunk.isupper():
                self.headdings.append(chunk)
                self.sections.append(len(self.raw_txt))
            elif chunk.startswith(FIG_TXT): # Whole Chunk will be the figure caption
                self.fig_capts.append(chunk)
                self.pre_fig.append(chunks[i-1]) if i != 0 else self.pre_fig.append("__TOP__")
            elif chunk.startswith(TAB_TXT): # Whole chunk will be table cpation
                self.table_capts.append(chunk)
            if chunk != "":
                self.raw_txt += chunk + '\n'
        
        # Find printed page number (if present)
        try:
            [tmp, pg_no] = self.raw_txt.strip().rsplit('\n',1)
            self.doc_page_numer == int(pg_no)
            self.raw_txt = f"\n--- PDF {page_index+1} DOC {pg_no} ---\n" + tmp
        except:
            self.raw_txt = f"\n--- PDF {page_index+1} DOC 0 ---\n" + self.raw_txt

    def has_figs(self)->bool:
        return len(self.fig_capts) > 0
        
# Used for testing
if __name__ == "__main__":
    if len(argv) == 2:
        print(f"Usage {argv[0]} <filename> <page-number")
        exit()
    file = argv[1]
    page_no = int(argv[2])

    with fitz.open(file) as doc:
        _time = timer()
        data = PageData(doc[page_no], page_no)
        _time = timer() - _time
        # print(data.raw_txt)
        print(f"Images:\n{data.fig_capts}")
        print(f"image xrefs: {len(data.img_xrefs)}")
        # print(f"headdings: {data.headdings}")
        # print(f"secion txt\n {data.get_section_txt()}")
        print(f"Time: {_time}")

