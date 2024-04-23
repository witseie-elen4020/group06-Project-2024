# This script conains serial code to extract all figures and text from a pdf page AND match figures to text 

import fitz
import os
import io
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import sqlite3

# ===================================
# General constants 

DB_FILE = "data.db"
LOG_FILE = "Logs.txt"
FIG_DIR = "Figures"
TEXT_DIR = "Text"

OUT_DIR = "Data"

# ===================================
def extract_from_doc(filename):


    fig_dir = os.path.join(OUT_DIR,FIG_DIR)
    if not os.path.exists(fig_dir):
        os.makedirs(fig_dir)
    with fitz.open(filename) as doc:
        # A good point to paralleis
        for page_no, page in enumerate(doc):
            extract_page(page_no, page, filename, doc)

def extract_page(page_index:int, page:fitz.Page, file_name:str, doc:fitz.Document):

    logs = ""

    # Extract all images from page
    image_list = page.get_images()

    # Extract all text from page 
    txt = page.get_text()

    [image_captions, table_captions] = get_captions(txt)

    if len(image_captions) > len(image_list):
        logs += f"Error: {len(image_captions)} Captions but only {len(image_list)} found.\n"

    for image_number, img in enumerate(image_list):
        if image_number >= len(image_captions):
            label = "unlabeled"
            fig_number = "0"
            caption = "none"
        else:
            [label, fig_number, caption] = (image_captions[image_number]).split(" ", 2)

        file_name = "Fig_" + fig_number + ".png"

        metadata = PngInfo()
        metadata.add_text("page", str(page_index))
        metadata.add_text("label", label)
        metadata.add_text("number", fig_number)
        metadata.add_text("caption", caption)
        metadata.add_text("document", file_name)

        save_path = os.path.join(OUT_DIR, FIG_DIR, file_name)
        base_image = doc.extract_image(xref=img[0])
        image_bytes = base_image["image"]
        image = Image.open(io.BytesIO(image_bytes))
        image.save(save_path, pnginfo=metadata)


    

# Retives the captions of all images from a block of text
# Retursn two lists of string captions and table caoptions along with line numbers
def get_captions(txt:str, fig_prefix:str = "Figure", tab_prefix:str = "Table"):
    lines = txt.split('\n') # Split text into lines
    # --- good point to paralise ---
    fig_captions = []
    tab_captions = []
    for line_no, line in enumerate(lines):
        if line.startswith(fig_prefix):
            fig_captions.append(line)
        elif line.startswith(tab_prefix):
            tab_captions.append(line)
    
    return fig_captions, tab_captions

