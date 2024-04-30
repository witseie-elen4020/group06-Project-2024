# This simple script is used to see the location of bounding boxes and text blocks in files 
# this helps refine infromation extraction processes
import fitz
import csv
import os
from sys import argv

if len(argv) == 2:
    print(f"Usage {argv[0]} <filename> <page-number")
    exit()
file = argv[1]
page_no = int(argv[2])

with fitz.open(file) as doc:

    # Get text blocks
    page = doc[page_no]

    textpage = page.get_textpage() #This is the most effective means of text extraction from a page 50% faster

    # textblocks
    blocks = page.get_text("blocks", textpage=textpage, sort=True)
    lines = []
    for blk in blocks:
        print("==== New block ===")
        print(blk)
        lines = lines + blk[4].split("\n")

