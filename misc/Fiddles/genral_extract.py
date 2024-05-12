# Simple protoype scipt used to test the effectivness of genral text, table and image extraction 

# This simple script is used to see how boundign boxeres can be denfied and used to extract table data
import fitz
from fitz import Rect
import csv
import os
from sys import argv

if len(argv) == 2:
    print(f"Usage {argv[0]} <filename> <page-number>")
    exit()
file = argv[1]
page_no = int(argv[2])

X_MAX = 595
Y_MAX = 842
MARGIN = 50

FIG_TXT = "Figure"
TAB_TXT = "Table"

with fitz.open(file) as doc:
    # Get text blocks
    page = doc[page_no]
    textpage = page.get_textpage() #This is the most effective means of text extraction from a page 50% faster
    
    bounds = page.bound()
    fig_captions = []
    table_captions = []
    page_x = bounds[2]
    page_y = bounds[3]
    if page_x <= X_MAX and page_y == Y_MAX:
        # Normal page size
        print("A4 Page Portrate")
        # Get text inside the margins
        txt = page.get_textbox(Rect(MARGIN, MARGIN, X_MAX-MARGIN, Y_MAX-MARGIN))

        # Find cunck instead of blocks becuase this has more reliable whitesapce behavior
        chunks = txt.replace("\n ","\n").split("\n\n")
        raw_txt = ""
        for chunk in chunks:
            chunk = ' '.join(chunk.split()).strip()
            if chunk.startswith(FIG_TXT):
                fig_captions.append(chunk)
            elif chunk.startswith(TAB_TXT):
                table_captions.append(chunk)

                # Now find table
                tab_capt_box = page.search_for(chunk)
                print(tab_capt_box)

            else:
                raw_txt+="=============="
                raw_txt += chunk

        #print(raw_txt)    
        # Find list of figure refferances
        image_xref_lst = page
            

    # Find tables
    tab_boxes = [page.search_for(t_capt)[0] for t_capt in table_captions]
    for tab_i, tab_box in enumerate(tab_boxes):
        maxy = Y_MAX if tab_i == len(tab_boxes)-1 else tab_boxes[tab_i+1][1] # Set table max y to the upperlimit of next table caption
        searach_box = Rect(0, tab_box[3]+30, page_x, maxy)
        tabs = page.find_tables(strategy="lines", clip=searach_box)
        if len(tabs.tables) == 0:
            print(f"Table Not found \n {table_captions[tab_i]}\n" )
            # Try a less strict apporch
            tabs = page.find_tables(strategy="text", clip=searach_box)
        print(len(tabs.tables))
        lines = tabs[0].extract()
        for line in lines:
            print(line)
                

    print("figurs:")
    print(fig_captions)
    print("tables:")
    print(table_captions)





