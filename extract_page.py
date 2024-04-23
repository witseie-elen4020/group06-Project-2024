# This script conains serial code to extract all figures and text from a pdf page AND match figures to text 

import fitz
import os
import io
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import sqlite3

from timeit import default_timer as timer # form benchmarking

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
    print(f"--- Page {page_index}")


    _time = timer()
    # Extract all images from page
    image_list = page.get_images()
    image_count = len(image_list)
    _time = timer()-_time
    print(f"Image extraction: {_time} for {image_count} images")

    # Extract all text from page 
    _time = timer()
    txt = page.get_text()
    _time = timer()-_time
    print(f"Text extraction: {_time} for {len(txt)} characters")


    # Find image captions (if any)
    _time = timer()
    [image_captions, table_captions] = get_captions(txt)
    image_capt_count = len(image_captions)
    _time = timer()-_time
    print(f"Caption extraction: {_time} for {image_capt_count} captions")

    if len(image_captions) > len(image_list):
        logs += f"Error: {len(image_captions)} Captions but only {len(image_list)} found.\n"

    _time = timer()
    fig_logs = ["Label", "Number", "Caption", "Document", "Path"]
    for image_number, img in enumerate(image_list):
        if image_number >= len(image_captions):
            label = "none"
            fig_number = "0"
            caption = "uncaptioned"
        else:
            [label, fig_number, caption] = (image_captions[image_number]).split(" ", 2)
            caption = caption.strip()

        #file_name = "Fig. " + fig_number.strip(".") + " " + caption.replace("/","-") + ".png"
        image_file_name = (os.path.basename(file_name))[:-4] + "_fig_" + fig_number.strip(".") + ".png"

        metadata = PngInfo()
        metadata.add_text("page", str(page_index))
        metadata.add_text("label", label)
        metadata.add_text("number", fig_number.strip("."))
        metadata.add_text("caption", caption)
        metadata.add_text("document", file_name)

        save_path = os.path.join(OUT_DIR, FIG_DIR, image_file_name)
        base_image = doc.extract_image(xref=img[0])
        image_bytes = base_image["image"]
        image = Image.open(io.BytesIO(image_bytes))
        image.save(save_path, pnginfo=metadata)

        # Add finger details to figure logs
        fig_logs.append([label, fig_number, caption, file_name, fig_number])

    _time = timer()-_time
    print(f"Image save: {_time} for {image_count} images")


    

# Retives the captions of all images from a block of text
# Retursn two lists of string captions and table caoptions along with line numbers
def get_captions(txt:str, fig_prefix:str = "Figure", tab_prefix:str = "Table"):
    lines = txt.split('\n') # Split text into lines
    # --- good point to paralise ---
    fig_captions = []
    tab_captions = []
    fig_capt = "" # Holds the caption being constructed
    for line_no, line in enumerate(lines):
        if line.startswith(fig_prefix) or (fig_capt != "" and line):
            fig_capt = fig_capt + line
            if (line.strip()).endswith(".") or not line:  # Assume that caption ends with a full stop
                fig_captions.append(fig_capt)
                fig_capt = ""
        elif line.startswith(tab_prefix):
            tab_captions.append(line)
    return fig_captions, tab_captions

