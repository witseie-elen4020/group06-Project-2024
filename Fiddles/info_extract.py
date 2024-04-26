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
    print(f"Title = {title_txt}")



