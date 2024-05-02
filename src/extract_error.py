# This script contains a simple class used to identify if an extraction error has occured during an operation

class ExtractionError(Exception):
    def __init__(self, msg:str, page_index:int) -> None:
        self.page_index = page_index
        super().__init__(msg)

    def __str__(self) -> str:
        return "ERROR! " + super().__str__() + f" On PDF page {self.page_index+1}"
    
class ExtractionNote(Exception): # Non critcal exception
    def __init__(self, msg:str, page_index:int) -> None:
        self.page_index = page_index
        super().__init__(msg)

    def __str__(self) -> str:
        return "Note. " + super().__str__() + f" On PDF page {self.page_index+1}"
    