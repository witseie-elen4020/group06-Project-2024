import os
import subprocess
import sys
import json

output_dir = "output"

def welcome_message():
    print("=======================================================")
    print("Welcome to the PDF Data Extraction Console Application!")
    print("=======================================================\n")

def get_file_path():
    return input("Please enter the path to your PDF file: ")

def run_backend_program(pdf_path, output_dir):
    # Adjust the execution command to use mpiexec
    process = subprocess.Popen(["mpiexec", "-n", "2", "python", "src/main_str.py", pdf_path, output_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
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
    print("4. View File Location")
    print("5. View Logs")
    print("6. Total Number of Images Extracted")
    print("7. Exit")

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

def main():
    welcome_message()
    pdf_path = get_file_path()
    stdout, stderr = run_backend_program(pdf_path, output_dir)
    # Print the output of the backend program
    print("\n=============")
    print("Script Output")
    print("=============\n")
    print(stdout)
    
    # Extract information from the JSON file
    json_file_path = os.path.join(output_dir, pdf_path, "info.json")
    if os.path.exists(json_file_path):
        info_data = extract_info_from_json(json_file_path)
    else:
        print("Info JSON file not found.")
        return

    while True:
        display_options()
        choice = input("Enter your choice (1-7): ")
        if choice == "1":
            print("\nTitle:", info_data.get("Title", "Title not found"))
        elif choice == "2":
            print("\nAuthors:", info_data.get("Authors", "Authors not found"))
        elif choice == "3":
            print("\nAbstract:", info_data.get("Abstract", "Abstract not found"))
        elif choice == "4":
            print("\nFile Location:", info_data.get("File", "File location not found"))
        elif choice == "5":
            view_logs(os.path.join(output_dir, pdf_path))
        elif choice == "6":
            figures_directory = os.path.join(output_dir, pdf_path, "Figures")
            print("\nTotal number of images extracted:", count_images(figures_directory))
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()
