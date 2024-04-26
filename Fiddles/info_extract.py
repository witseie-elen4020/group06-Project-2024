# A simple text script used to refine genral document information and exploit the genral formatitng trends of the first 4 pages

# This simple script is used to see how boundign boxeres can be denfied and used to extract table data
import fitz
from fitz import Rect
import csv
import os
from sys import argv

# Page dimations for A4
X_MAX = 595
Y_MAX = 842

TITLE_RECT = Rect(180, 450, X_MAX, 520)
AUTOR_RECT = Rect(180, 535, X_MAX, 620)

ABSTRACT_START_TXT = "ABSTRACT"
END_TXT = "_oOo_"

if len(argv) == 1:
    print(f"Usage {argv[0]} <filename>")
    exit()
file = argv[1]

with fitz.open(file) as doc:

    # === Page 1 === 
    page = doc[0]
    textpage = page.get_textpage()

    # Attempt to locate title
    title_txt = page.get_textbox(TITLE_RECT, textpage=textpage)
    title_txt = ' '.join(title_txt.split())
    print(f"Title = {title_txt}\n")

    # Attempt to find authors
    authors_txt = page.get_textbox(AUTOR_RECT, textpage=textpage)
    authors_txt = authors_txt.strip()
    authors_txt = " ".join(authors_txt.replace("\n", ",").replace(" AND", ",").split()).replace(",,",",").replace(", ,",",") # Ensure that list of authors is seperated by commas only
    print(f"Authors = {authors_txt}\n")

    # === Page 2 ====
    # Get date
    page = doc[1]
    textpage = page.get_textpage()
    txt = page.get_text("text", textpage=textpage)
    # Locate date
    date_txt = txt.strip().rsplit("\n", 1)[-1]
    print(f"Date = {date_txt}\n")


    # === Page 3 ===
    # Get abstrct
    page = doc[2]
    textpage = page.get_textpage()

    abstract_start = page.search_for(ABSTRACT_START_TXT, textpage=textpage)
    abstract_end = page.search_for(END_TXT, textpage=textpage)

    abstract_rect = Rect(0, abstract_start[0][3], X_MAX, abstract_end[0][1])
    abstract_rect.bottom_left
    abstract_txt = page.get_textbox(abstract_rect).strip()

    print("Abstract")
    print(abstract_txt, "\n")

