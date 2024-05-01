# Contains the defiation for extraction jobs based on job strings

SPLIT_STR = ")-("
ROJ_SPLIT_S = "|+"  #first half of run on job
ROJ_SPLIT_E = "+|"   # second hald of run on job

IMG_TAG = "IMG"
ABSTRACT_TAG = "ABS"


# Returns an extraction job fo image retreval
def get_img_job_str(caption:str, xref:int, pdf_pg:str, doc_pg:str):
    return SPLIT_STR.join([caption, str(xref), pdf_pg, doc_pg])
# A string to indicate the start of the abstract job

def get_abs_start_str():
    return ABSTRACT_TAG + SPLIT_STR

def get_job(job_str):
    return
