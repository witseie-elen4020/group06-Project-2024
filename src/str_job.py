# Contains the defiation for extraction jobs based on job strings
from typing import List
import os
import io

import fitz
from PIL import Image
from PIL.PngImagePlugin import PngInfo

from doc_data import DocData

SPLIT_STR = ")-("
ROJ_SPLIT_S = "|+"  #first half of run on job
ROJ_SPLIT_E = "+|"   # second hald of run on job

IMG_TAG = "IMG"
ABSTRACT_TAG = "ABS"


IMG_DIR = "Figures"

# Returns an extraction job fo image retreval
def get_img_job_str(caption:str, xref:int, pdf_pg:str, doc_pg:str):
    return SPLIT_STR.join([IMG_TAG, caption, str(xref), pdf_pg, doc_pg])
# A string to indicate the start of the abstract job

def get_abs_start_str():
    return ABSTRACT_TAG + SPLIT_STR

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

class ImgJob:
    def __init__(self, job_str:str) -> None:
        [tag, self.capt, self.xref, self.pdf_pg, self.doc_pg] = job_str.split(SPLIT_STR)
        assert(tag == IMG_TAG)
    def do_job(self, doc:fitz.Document, file_name:str, save_path):
        # Split inamge catption into useful chuncks
        [label, fig_number, caption] = (self.capt).split(" ", 2)

        image_file_name = "fig_" + fig_number.strip(".").strip(":") + ".png"


        metadata = PngInfo()
        metadata.add_text("PDF page", str(self.pdf_pg))
        metadata.add_text("DOC page", str(self.doc_pg))
        metadata.add_text("label", label)
        metadata.add_text("number", fig_number.strip("."))
        metadata.add_text("caption", caption)
        metadata.add_text("document", file_name)

        save_path = os.path.join(save_path, IMG_DIR,image_file_name)

        base_image = doc.extract_image(xref=int(self.xref))
        image_bytes = base_image["image"]
        image = Image.open(io.BytesIO(image_bytes))
        image.save(save_path, pnginfo=metadata)


