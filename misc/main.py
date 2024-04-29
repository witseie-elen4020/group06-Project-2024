import fitz
import os
import sqlite3

def extract_captions(txt_file, prefix):
    with open(txt_file, "r") as file:
        caption = []
        for line in file:
            line = line.strip()
            if line.startswith(prefix):
                caption.append(line)
            elif caption and line:  
                caption.append(line)
            elif caption and not line:  
                yield " ".join(caption)
                caption = []
        if caption:  
            yield " ".join(caption)

def find_items(pdf_file, output_dir, db_file):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with fitz.open(pdf_file) as doc:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS figures
                     (page INTEGER, caption TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS tables
                     (page INTEGER, caption TEXT)''')
        
        for page_index, page in enumerate(doc):
            page_text = page.get_text()
            with open(f"{output_dir}/page_{page_index+1}.txt", "w") as txt_file:
                txt_file.write(page_text)
            figure_captions = extract_captions(f"{output_dir}/page_{page_index+1}.txt", "Figure")
            for caption in figure_captions:
                print(f"Page {page_index+1}: {caption}")
                c.execute("INSERT INTO figures VALUES (?, ?)",
                          (page_index+1, caption))
            table_captions = extract_captions(f"{output_dir}/page_{page_index+1}.txt", "Table")
            for caption in table_captions:
                print(f"Page {page_index+1}: {caption}")
                c.execute("INSERT INTO tables VALUES (?, ?)",
                          (page_index+1, caption))
        conn.commit()
        conn.close()

find_items("data/390.pdf", "pages", "figures.db")