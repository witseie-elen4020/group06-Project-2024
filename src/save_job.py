# this script contians a list of data save jobs woch can be enqued for parallel processing
import fitz
from fitz import Rect

from PIL import Image
from PIL.PngImagePlugin import PngInfo

from doc_data import DocData
from page_data import PageData

import os, io
from sys import argv
from typing import List

from timeit import default_timer as timer # form benchmarking

FIG_DIR = "Figures"

# Page dimations for A4
X_MAX = 595
Y_MAX = 842


# Class used to 
class ImgSaveJob:
    def __init__(self, page_data:PageData, doc_data:DocData) -> None:
        self.page_data = page_data
        self.doc_data = doc_data
        self.log = []


    # Called to execute image save job
    def execute(self, doc:fitz.Document)->List[str]:
        
        if len(self.page_data.fig_capts) == 0:
            return ["No Images to be saved"]
        # Get image xrefs
        xrefs = self.page_data.img_xrefs
        capts = self.page_data.fig_capts
        
        if len(xrefs) != len(self.page_data.fig_capts):
            xrefs = []
            capts = []
            # Some images are missing - iterate through captions to see which caption has no corresponding image
            for i,capt in enumerate(self.page_data.fig_capts):
                capt_box = self.page_data.textpage.search(capt)[0] # Bounding rect of caption
                pre_box = self.page_data.textpage.search(self.page_data.pre_fig[i])[0] if self.page_data.pre_fig[i] != "__TOP__" else Rect(0, 0, X_MAX , Y_MAX)# bounding box of text above caption
                fig_box = Rect(0, pre_box[3], X_MAX, capt_box[1]) # Fingure must be contained in this boudning box
                xref = doc[self.page_data.page_index].get_images(fig_box)
                if len(xref) == 0:
                    self.logs.append(f"Figure with caption '{capt}' not found.")
                else:
                    xrefs.append(xref[0])
                    capts.append(capt) 
            
        
        # Now save all valid images
        doc_data.make_dir(FIG_DIR)
        for image_number, xref in enumerate(xrefs):
            [label, fig_number, caption] = (capts[image_number]).split(" ", 2)
            caption = caption.strip()

            image_file_name = "fig_" + fig_number.strip(".").strip(":") + ".png"

            metadata = PngInfo()
            metadata.add_text("PDF page", str(self.page_data.page_index))
            metadata.add_text("DOC page", str(self.page_data.doc_page_numer))
            metadata.add_text("label", label)
            metadata.add_text("number", fig_number.strip("."))
            metadata.add_text("caption", caption)
            metadata.add_text("document", self.doc_data.file_name)

            save_path = os.path.join(self.doc_data.save_path, FIG_DIR, image_file_name)

            print(xref[0])
            base_image = doc.extract_image(xref=xref[0])
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            image.save(save_path, pnginfo=metadata)

            return self.log
        

# For testing purposes 
if __name__ == "__main__":
    if len(argv) == 2:
        print(f"Usage {argv[0]} <filename> <page-number>")
        exit()
    file = argv[1]
    page_no = int(argv[2])

    with fitz.open(file) as doc:
        data = PageData(doc[page_no], page_no)
        doc_data = DocData(file, "TMP_TEST")
        _time = timer()
        logs =[]
        if data.has_figs():
            save_job = ImgSaveJob(data, doc_data)
            logs = save_job.execute(doc)
        _time = timer() - _time
        print(data.raw_txt)
        print(f"Logs:\n{logs}")
        print(f"image xrefs: {len(data.img_xrefs)}")
        # print(f"image xrefs: {len(data.img_xrefs)}")
        # print(f"headdings: {data.headdings}")
        # print(f"secion txt\n {data.get_section_txt()}")
        print(f"Time: {_time}")

    


