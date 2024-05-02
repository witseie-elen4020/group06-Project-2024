# This script contains code to perfrom serail pdf extraction for the sake of comparison 
import os

from mpi4py import MPI  # Import MPI module for parallel computing
import fitz  # Import fitz module for PDF processing
from fitz import Rect
from sys import argv  # Import argv for command-line arguments
from page_data import PageData  # Import the PageData class 

from timeit import default_timer as timer # form benchmarking
from extract_error import ExtractionError, ExtractionNote
import str_job
from doc_data import DocData


# Key words to look for 
ABSTRACT_START_TXT = "ABSTRACT"
CONTENT_START_TXT = "CONTENTS "
PAGE_TXT = "Page"
END_TXT = "_oOo_"

# Very similar to the parallel case
def extract_doc_info(doc:fitz.Document, page_index:int):
    raw_txt = ""        # Holds all text from page (including figure captions)
    log = ""            # Holds a record of any error that may occure

    #for page in doc:



    contents = ""       # Holds section headdings and text, (without figure captions)
    numbers = ""        # Holds information realting to document page numbers
    jobs = ""           # Holds information realting to futher extraction jobs
    

    fig_capts = []     # Holds figure caption
    doc_pg_no = 0

    # Flags
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
            
            # Set captions and xrefs to good ones
            fig_capts = good_capts
            img_xrefs = good_xrefs
            
        # Now make image jobs
        assert(len(fig_capts) == len(img_xrefs))

        for capt_i, capt in enumerate(fig_capts):
            jobs += str_job.get_img_job_str(capt, img_xrefs[capt_i][0], str(page_index), str(doc_pg_no)) + MAJOR_BREAK
                
    except ExtractionError as e:
        log += str(e) + '\n'
    except ExtractionNote as e:
        log += str(e) + '\n'
     
    return raw_txt, contents, numbers, jobs, log  