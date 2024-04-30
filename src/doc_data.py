import os

# Simple call whaich contins document data such as save directory and file name
class DocData:
    def __init__(self, input_path:str, output_path:str = "Output") -> None:
        self.input_path = input_path
        self.file_name = os.path.basename(input_path)
        self.file_label = self.file_name.rsplit('.', 1)[0]
        self.save_path = os.path.join(output_path, self.file_label)

    def __str__(self) -> str:
        return f"{self.file_name}"
    
    def make_dir(self,path:str):
        dir_path = os.path.join(self.save_path, path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)