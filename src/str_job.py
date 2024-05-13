# Contains the defiation for extraction jobs based on job strings
from typing import List
import os
import io
import json
import csv

import fitz
from PIL import Image
from PIL.PngImagePlugin import PngInfo

from extract_error import ExtractionError, ExtractionNote

SPLIT_STR = ")-("
ROJ_SPLIT_S = "|+"  #first half of run on job
ROJ_SPLIT_E = "+|"   # second hald of run on job

# Images 
IMG_TAG = "IMG"
IMG_DIR = "Figures"
IMG_FILE = "figure_captions.txt"
FIG_TXT = "Figure"

# Tables 
TABLE_TAG = "TAB"
TAB_FILE = "table_captions.txt"

# Content ans sections
TEXT_TAG = "TXT"
TEXT_FILE = "text.txt"
CONTENT_TAG = "CON"
CONTENT_DIR = "Sections"
CONTENT_FILE = "content.json"
# Docuemnt info
INFO_TAG = "INF"
INFO_FILE = "info.json"

# -- For text fromatting --
GLOBAL_BREAK = ">>x<<"
MAJOR_BREAK = "]==["
MINOR_BREAK = ")--("

# -- For writng styles ---
# Captions 
FIG_TXT = "Figure"
TAB_TXT = "Table"

# genral structure
EXPECTED_ABSTRACT = 2
MAX_ABSTRACT = 3
EXPECTED_CONTENT = 3
MAX_CONTENT = 4

# Key words to look for 
ABSTRACT_START_TXT = "ABSTRACT"
CONTENT_START_TXT = "CONTENTS "
PAGE_TXT = "Page"
END_TXT = "_oOo_"


# Returns an extraction job fo image retreval
def get_img_job_str(caption:str, xref:int, pdf_pg:str, doc_pg:str):
    return SPLIT_STR.join([IMG_TAG, caption, str(xref), pdf_pg, doc_pg])

# Formats a table extraction job as a string
def get_table_job_str(caption:str, ypos:int, pdf_pg:str, doc_pg:str):
    return SPLIT_STR.join([TABLE_TAG, caption, ypos, pdf_pg, doc_pg])

def get_jobs(job_strs:List[str]):
    jobs = []
    for job_str in job_strs:
        if job_str.startswith(IMG_TAG):
            jobs.append(ImgJob(job_str))
        elif job_str == "" or job_str.isspace():
            continue
        else:
            print(f"TODO unknow job {job_str[:3]}")
    return jobs


def get_job(job_str:str):
    if job_str.startswith(IMG_TAG):
        return ImgJob(job_str)
    else:
        print(f"TODO unknow job {job_str[:3]}")

# Jobs used for extracting and saving an image 
class ImgJob:
    def __init__(self, job_str:str) -> None:
        [tag, self.capt, self.xref, self.pdf_pg, self.doc_pg] = job_str.split(SPLIT_STR)
        assert(tag == IMG_TAG)
    def do_job(self, doc:fitz.Document, file_name:str, save_path):
        # Split inamge catption into useful chuncks
        log = ""
        [label, fig_number, caption] = (self.capt).split(" ", 2)

        # Ensure that figure number is numeric
        fig_number = fig_number.strip(".").strip(":")
        try:
            fig_int = int(fig_number)
        except:
            try: 
                fig_int = int(label.strip(FIG_TXT).strip(".").strip(":"))
                fig_number = label.strip(FIG_TXT).strip(".").strip(":")
            except:
                log = f"Figure with number non-numeric number '{fig_number}' on pdf page {int(self.pdf_pg)+1}."
        image_file_name = "fig_" + fig_number + ".png"



        metadata = PngInfo()
        metadata.add_text("PDF page", str(int(self.pdf_pg)+1))
        metadata.add_text("DOC page", self.doc_pg)
        metadata.add_text("label", label)
        metadata.add_text("number", fig_number)
        metadata.add_text("caption", caption)
        metadata.add_text("document", os.path.basename(file_name))

        save_path = os.path.join(save_path, IMG_DIR,image_file_name)

        base_image = doc.extract_image(xref=int(self.xref))
        image_bytes = base_image["image"]
        image = Image.open(io.BytesIO(image_bytes))
        image.save(save_path, pnginfo=metadata)

        return log

# Extracts and save genral page information such as title and author
class InfoJob:
    def __init__(self, info_str:str, maj_split:str, min_split:str) -> None:
        self.info = info_str.strip(INFO_TAG+SPLIT_STR)
        self.maj = maj_split
        self.min = min_split
        pass

    def do_job(self, doc:fitz.Document, file_name:str, save_path):
        # Split fist docuemnt section into is subsection
        secs = self.info.split(self.maj)
        try:
            # The final section should be the abstract
            [title, abstract] = secs[-1].replace(self.min,"").split("ABSTRACT")
            
            abstract = abstract.strip("ABSTRACT")

            offset = 0
            if title == "" or  title.isspace():
                title = secs[-2].strip(self.min)
                offset = 1

            # The penultimate section cantaisn the date
            date = secs[-(2+offset)].strip().rsplit('\n', 1)[-1]

            # The second section contains the authors, the exact splitting is inconsitent here so third section is also included
            authors = "".join(secs[1:3]).split(self.min,2)[1].split("\n",1)[0].replace(" AND", ",")
            info = {
                    "Title": title,
                    "Authors": authors,
                    "Date": date,
                    "Abstract": abstract,
                    "File": file_name
                }
            with open(os.path.join(save_path, INFO_FILE), "w") as file:
                json.dump(info, file)
            return ""
        except:
            return "ERROR! Page infromation not found"

    # Saves raw text into a single file
    class TxtJob:
        def __init__(self, txt:str) -> None:
            self.txt = txt.strip(TEXT_TAG+SPLIT_STR)

        def do_job(self, doc:fitz.Document, file_name:str, save_path):

            with open(os.path.join(save_path, TEXT_FILE), "w") as file:
                file.write(self.txt)


# Save table of content and each section as a sub-directory
class ContentJob:
    def __init__(self, content_str:str, maj_split:str, min_split:str) -> None:
        self.content_str = content_str  # Holds table of content
        self.maj = maj_split
        self.min = min_split

    def do_job(self, doc:fitz.Document, file_name:str, save_path):

        try:
        
            # Fist section of contents is the title
           # [title, self.content_str] = title = self.content_str.split(self.maj, 1)

            main_secs = self.content_str.split("Page", 1)[1].strip().split(self.maj)
            content = {}
            for sec in main_secs:
                if sec == "":
                    continue
                try:
                    [headding, remainder] = sec.split(self.min,1)
                except:
                    [headding, remainder] = sec.split('\n',1)
                number = remainder.split('\n',1)[0]
                content[headding] = number
                

            with open(os.path.join(save_path, CONTENT_FILE), "w") as file:
                json.dump(content, file)

            return ""
        except:
            return "ERROR! Contents not found\n"  
        
# Job calss aossated with extracting and saving tables from a given page. This can be tedious
class TableJob:
    def __init__(self, job_str:str) -> None:
        [tag, self.capt, self.pdf_pg, self.doc_pg] = job_str.split(SPLIT_STR)
        assert(tag == TABLE_TAG)


# Functionnused tor extraxt text and job information from a given pdf page
def extract_page_info(page:fitz.Page, page_index:int):
    raw_txt = ""        # Holds all text from page (including figure captions)
    contents = ""       # Holds section headdings and text, (without figure captions)
    numbers = ""        # Holds information realting to document page numbers
    jobs = ""           # Holds information realting to futher extraction jobs
    figs_str = ""       # Stores all figure captions
    tabs_str = ""       # Holds all table captions
    log = ""            # Holds a record of any error that may occure

    fig_capts = []      # Holds figure caption
    tab_cpats = []      # Holds table captions
    doc_pg_no = 0

    # Flags
    roj_end = False # run on job ends on this page
    roj_start = False # run on job start on this page
    hide_flag = False # Content should not be written to a section

    textpage = page.get_textpage()  # Use a textpage for faster text extraction 
    txt = textpage.extractText(sort=True)
    # Find chunck instead of blocks becuase this has more reliable whitesapce behavior
    chunks = txt.replace("\n ","\n").split("\n\n")
    for i,chunk in enumerate(chunks):
        chunk = ' '.join(chunk.split()).strip() # Clean chunck
        if chunk.isupper(): # Indcative of a headding
            contents += MAJOR_BREAK + chunk + MINOR_BREAK # Add section start to headding
            hide_flag = True
        elif chunk.startswith(FIG_TXT): # Whole Chunk will be the figure caption
            fig_capts.append(chunk)
            hide_flag = True
        elif chunk.startswith(TAB_TXT):
            # Add table caption to captions list 
            tab_cpats.append(chunk)
        elif chunk.startswith(TAB_TXT) and 1==2: # Whole chunk will be table cpation
            assert(False)
        elif END_TXT in chunk:
            contents = contents + GLOBAL_BREAK
            hide_flag = True
        if chunk != "":
            raw_txt += chunk + '\n'
            if page_index <= MAX_CONTENT and not hide_flag:
                contents += chunk + '\n'
        # Reset hide flag to false
        hide_flag = False
        
    # Find printed page number (if present)
    try:
        [tmp, pg_no] = raw_txt.strip().rsplit('\n',1)
        doc_pg_no = int(pg_no)
        numbers = f"--- PDF {page_index+1} DOC {doc_pg_no} ---"
        raw_txt = f"\n{numbers}\n" + tmp
    except:
        numbers = f"--- PDF {page_index+1} DOC 0 ---"
        raw_txt = f"\n{numbers}\n" + raw_txt

            
    # Write figure and tabke coations to corresponding strings.
    for fig_capt in fig_capts:
        # Add figure caption to captios list (this should happen regairdless of wether the figure was found or not)
        figs_str += '\t\t'.join([fig_capt,"PDF_page:"+str(page_index+1),"DOC_page:"+str(doc_pg_no)]) + '\n'

    for tab_capt in tab_cpats:
        tabs_str += '\t\t'.join([tab_capt,"PDF_page:"+str(page_index+1),"DOC_page:"+str(doc_pg_no)]) + '\n'
        

    # Find images to be extracted and creat correspoding jobs
    try:
        # Get figure xrefs for extraction
        img_xrefs = page.get_images()

        capt_count = len(fig_capts)
        xref_count = len(img_xrefs)
    
        if capt_count != xref_count: # Chack to see if all images were found
            if capt_count == 0:
                raise ExtractionNote(f"Ignored {xref_count} uncaptioned images", page_index)
            elif capt_count == 1:
                raise ExtractionError(f"Could not find image with caption: '{fig_capts[0][:20]}...' ", page_index)
            
            # More than one figure, detemine which images are captioned
            good_xrefs = []
            good_capts = []
            # The bounding boxes of all page captions 
            capt_bbs = [page.search_for(capt, textpage=textpage)[0] for capt in fig_capts]
            for capt_i, bb in enumerate (capt_bbs):
                
                # Bounds of figure location
                ymin = 0 if capt_i == 0 else capt_bbs[capt_i-1][3]
                ymax = bb[1]

                _capt_images = [xref for xref in img_xrefs if (xref[2] > ymin and xref[2] < ymax)]

                if(len(_capt_images) == 0):
                    log += str(ExtractionError(f"Could not find image with caption: '{fig_capts[capt_i][:20]}...' ", page_index))+'\n'
                    continue
                elif(len(_capt_images) > 1):
                    log += str(ExtractionNote(f"Ignored {len(_capt_images -1 )} uncaptioned images above figure caption {fig_capts[capt_i][:20]}...'", page_index))+'\n'
                
                # Assume valid image to be the lowest one
                good_capts.append(fig_capts[capt_i])
                good_xrefs.append(_capt_images[-1])
            
            # Set captions and xrefs to those which have been found
            fig_capts = good_capts
            img_xrefs = good_xrefs
            
        # Now make image jobs
        assert(len(fig_capts) == len(img_xrefs))

        for capt_i, capt in enumerate(fig_capts):
            jobs += get_img_job_str(capt, img_xrefs[capt_i][0], str(page_index), str(doc_pg_no)) + MAJOR_BREAK
                
    except ExtractionError as e:
        log += str(e) + '\n'
    except ExtractionNote as e:
        log += str(e) + '\n'

     
    return raw_txt, contents, numbers, jobs, figs_str, tabs_str, log  