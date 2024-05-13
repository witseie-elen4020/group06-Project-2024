import os
import subprocess
import sys
import json
import glob
from PIL import Image
from pprint import pprint
import questionary
from colorama import Fore, Style

output_dir = "output"

os.system("clear")

def welcome_message():
    print(Fore.YELLOW + "=======================================================")
    print("Welcome to the PDF Data Extraction Console Application!")
    print("=======================================================\n" + Style.RESET_ALL)

def get_file_path():
    choice = questionary.select(
        "How would you like to specify the PDF file?",
        choices=[
            'Enter the complete file path',
            'Specify a directory and select a PDF'
        ]).ask()

    if choice == 'Enter the complete file path':
        return input("Please enter the path to your PDF file: ")
    elif choice == 'Specify a directory and select a PDF':
        directory = input("Please enter the directory: ")
        pdf_files = glob.glob(os.path.join(directory, '*.pdf'))
        if not pdf_files:
            print("No PDF files found in the specified directory.")
            return None
        return questionary.select(
            "Please select a PDF file:",
            choices=pdf_files
        ).ask()

def run_backend_program(pdf_path, output_dir):
    # Adjust the execution command to use mpiexec
    process = subprocess.Popen(["mpiexec", "-n", "4", "python", "src/main_str.py", pdf_path, output_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    return stdout, stderr

def extract_info_from_json(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    return data

def view_logs(pdf_directory):
    logs_path = os.path.join(pdf_directory, "log.txt")
    if os.path.exists(logs_path):
        with open(logs_path, "r") as file:
            # print("\n=================")
            # print("Logs from log.txt")
            # print("=================\n")
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

def display_options():
    return questionary.select(
        "Select an option to view:",
        choices=[
            'View Report Title',
            'View Report Authors',
            'View Abstract',
            'View Figures Captions',
            'View Figures Metadata',
            'View Table Captions',
            'View File Location',
            'View Logs',
            'Exit'
        ]).ask()

def main():
    welcome_message()
    pdf_path = get_file_path()

    # Check that file path is valid
    while not os.path.exists(pdf_path): 
        print(f"PDF file '{pdf_path}' not found.")
        pdf_path = get_file_path()

    stdout, stderr = run_backend_program(pdf_path, output_dir)
    # Print the output of the backend program
    print(Fore.CYAN + "\n=============")
    print("Script Output")
    print("=============\n" + Style.RESET_ALL)
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

    print(f"\nThe script has run successfully. Results for report '{Fore.GREEN}{info_data.get('Title', 'Title not found')}{Style.RESET_ALL}' have been stored in directory '{Fore.GREEN}output{Style.RESET_ALL}'")

    print("\nYou can now view the extracted information from the PDF file.\n")
    while True:
        choice = display_options()
        if choice == "View Report Title":
            print("\n" + Fore.YELLOW + "="*30)
            print("TITLE".center(30))
            print("="*30 + "\n" + Style.RESET_ALL)
            print("\n" + Fore.YELLOW + "Title:".ljust(10) + Style.RESET_ALL,info_data.get("Title", "Title not found"))
            print("\n")
        elif choice == "View Report Authors":
            print("\n" + Fore.YELLOW + "="*30)
            print("AUTHORS".center(30))
            print("="*30 + "\n" + Style.RESET_ALL)
            print("\n" + Fore.YELLOW + "Authors:".ljust(10) + Style.RESET_ALL, info_data.get("Authors", "Authors not found"))
            print("\n")
        elif choice == "View Abstract":
            print("\n" + Fore.YELLOW + "="*30)
            print("ABSTRACT".center(30))
            print("="*30 + "\n")
            print(Fore.YELLOW + "Abstract:".ljust(10) + Style.RESET_ALL, info_data.get("Abstract", "Abstract not found"))
        elif choice == "View Figures Captions":
            print("\n" + Fore.YELLOW + "="*30)
            print("FIGURES CAPTIONS".center(30))
            print("="*30 + Style.RESET_ALL + "\n")
            figures_directory = os.path.join(output_dir, pdf_path_base, "Figures")
            print("\nTotal number of images extracted:", count_images(figures_directory))
            print_captions_in_directory(figures_directory)
        elif choice == "View Figures Metadata":
            print("\n" + Fore.YELLOW + "="*30)
            print("FIGURES METADATA".center(30))
            print("="*30 + Style.RESET_ALL + "\n")
            figures_directory = os.path.join(output_dir, pdf_path_base, "Figures")
            print_image_metadata_in_directory(figures_directory)
        elif choice == "View Table Captions":
            print("\n" + Fore.YELLOW + "="*30)
            print("TABLE CAPTIONS".center(30))
            print("="*30 + Style.RESET_ALL + "\n")
            figures_directory = os.path.join(output_dir, pdf_path_base)
            view_table_captions(figures_directory)
        elif choice == "View File Location":
            print("\n" + Fore.YELLOW + "="*30)
            print("FILE LOCATION".center(30))
            print("="*30 + "\n")
            print("\n" + Fore.YELLOW + "File Location:".ljust(10) + Style.RESET_ALL, info_data.get("File", "File location not found"))
            print("\n")
        elif choice == "View Logs":
            print("\n" + Fore.YELLOW + "="*30)
            print("LOGS".center(30))
            print("="*30 + Style.RESET_ALL + "\n")
            view_logs(os.path.join(output_dir, pdf_path_base))
        elif choice == "Exit":
            print(f"{Fore.RED}Exiting...{Style.RESET_ALL}")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main()
