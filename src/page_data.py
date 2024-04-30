# Contains class definetions which can aid in page 
import fitz
from fitz import Rect
import os
import io
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

        # initalis lists
        self.fig_capts = []
        self.table_capts = []

        txt = self.textpage.get_text()
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
                self.ended = True
                self.completed = self.abstract_start
            if chunk.startswith(FIG_TXT):
                self.fig_capts.append(chunk)
            elif chunk.startswith(TAB_TXT):
                self.table_capts.append(chunk)

            self.raw_txt += chunk

            self.fig_xrefs = page.get_images()
