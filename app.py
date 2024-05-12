import os
import subprocess
import sys
import json
from PIL import Image
from pprint import pprint

output_dir = "output"

def welcome_message():
    print("=======================================================")
    print("Welcome to the PDF Data Extraction Console Application!")
    print("=======================================================\n")

def get_file_path():
    return input("Please enter the path to your PDF file: ")

def run_backend_program(pdf_path, output_dir):
    # Adjust the execution command to use mpiexec
    process = subprocess.Popen(["mpiexec", "-n", "4", "python", "src/main_str.py", pdf_path, output_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    return stdout, stderr

def extract_info_from_json(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    return data

def display_options():
    print("\nSelect an option to view:")
    print("1. View Report Title")
    print("2. View Report Authors")
    print("3. View Abstract")
    print("4. View Figures Captions")
    print("5. View Figures Metadata")
    print("6. View Table Captions")
    print("7. View File Location")
    print("8. View Logs")
    print("9. Exit")
    

def view_logs(pdf_directory):
    logs_path = os.path.join(pdf_directory, "log.txt")
    if os.path.exists(logs_path):
        with open(logs_path, "r") as file:
            print("\n=================")
            print("Logs from log.txt")
            print("=================\n")
            print(file.read())
    else:
        print("Logs file not found.")

def count_images(figures_directory):
    images_count = 0
    if os.path.exists(figures_directory):
        for root, dirs, files in os.walk(figures_directory):
            images_count += len(files)
    return images_count

def extract_caption(image_path):
    with Image.open(image_path) as img:
        metadata = img.info
        caption = metadata.get("caption")
    return caption

def print_captions_in_directory(directory):
    if not os.path.isdir(directory):
        print("Invalid directory path.")
        return

    image_files = [f for f in os.listdir(directory) if f.endswith('.png')]
    if not image_files:
        print("No PNG images found in the directory.")
        return

    # Sort image files by their numeric part
    image_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))

    for image_file in image_files:
        image_path = os.path.join(directory, image_file)
        caption = extract_caption(image_path)
        print(f"\nImage: {image_file}")
        if caption:
            print("Caption:", caption)
        else:
            print("No caption found.")
        print()

from PIL import Image
from pprint import pprint
import os

def print_image_metadata_in_directory(directory):
    if not os.path.isdir(directory):
        print("Invalid directory path.")
        return

    image_files = [f for f in os.listdir(directory) if f.endswith('.png')]

    if not image_files:
        print("No PNG images found in the directory.")
        return

    # Sort image files by their numeric part
    image_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))

    for image_file in image_files:
        image_path = os.path.join(directory, image_file)
        metadata = extract_metadata(image_path)

        print(f"\nImage: {image_file}")
        pprint(metadata)
        print()

def extract_metadata(image_path):
    with Image.open(image_path) as img:
        metadata = img.info

    return metadata

def view_table_captions(pdf_directory):
    print() 
    table_captions_path = os.path.join(pdf_directory, "table_captions.txt")
    if os.path.exists(table_captions_path):
        with open(table_captions_path, "r") as file:
            lines = file.readlines()
            num_tables = len(lines)
            print(f"Total number of tables detected: {num_tables}")
            for i, line in enumerate(lines, start=1):
                columns = line.strip().split("\t")
                caption = columns[0]
                pdf_page = columns[2]
                doc_page = columns[4]
                print(f"Table {i}:")
                print(f"Caption: {caption}")
                print(f"PDF Page: {pdf_page.split(':')[-1]}")
                print(f"DOC Page: {doc_page.split(':')[-1]}")
                print()
            # for line in file:
            #     columns = line.strip().split("\t")
            #     caption = columns[0]
            #     pdf_page = columns[2]
            #     doc_page = columns[4]
            #     print(f"{caption}")
            #     print(f"PDF Page: {pdf_page}")
            #     print(f"DOC Page: {doc_page}")
            #     print()
    else:
        print("Table captions file not found.")

def main():
    welcome_message()
    pdf_path = get_file_path()

    # Check that file path is valid
    while not os.path.exists(pdf_path): 
        print(f"PDF file '{pdf_path}' not found.")
        pdf_path = get_file_path()

    stdout, stderr = run_backend_program(pdf_path, output_dir)
    # Print the output of the backend program
    print("\n=============")
    print("Script Output")
    print("=============\n")
    print(stdout)
    
    # Change pdf file to be base path
    pdf_path_base = os.path.splitext(os.path.basename(pdf_path))[0]
    # Extract information from the JSON file
    json_file_path = os.path.join(output_dir, pdf_path_base, "info.json")
    if os.path.exists(json_file_path):
        info_data = extract_info_from_json(json_file_path)
    else:
        print("Info JSON file not found.")
        return

    while True:
        display_options()
        choice = input("Enter your choice (1-9): ")
        if choice == "1":
            print("\nTitle:", info_data.get("Title", "Title not found"))
        elif choice == "2":
            print("\nAuthors:", info_data.get("Authors", "Authors not found"))
        elif choice == "3":
            print("\nAbstract:", info_data.get("Abstract", "Abstract not found"))
        elif choice == "4":
            figures_directory = os.path.join(output_dir, pdf_path_base, "Figures")
            print("\nTotal number of images extracted:", count_images(figures_directory))
            print_captions_in_directory(figures_directory)
        elif choice == "5":
            figures_directory = os.path.join(output_dir, pdf_path_base, "Figures")
            print_image_metadata_in_directory(figures_directory)
        elif choice == "6":
            figures_directory = os.path.join(output_dir, pdf_path_base)
            view_table_captions(figures_directory)
        elif choice == "7":
            print("\nFile Location:", info_data.get("File", "File location not found"))
        elif choice == "8":
            view_logs(os.path.join(output_dir, pdf_path_base))
        elif choice == "9":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main()
