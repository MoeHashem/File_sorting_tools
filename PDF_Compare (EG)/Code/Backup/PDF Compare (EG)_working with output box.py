#########################################################################
#UPDATE INPUTS BELOW AS NEEDED !!
#First time users: type "pip install PyPDF2" in the terminal below (VSCode) or in the comand prompt if using Notepad

###INPUTS####
# Make sure the parent folder only contains subfolders (no actual files in parent folder)
# folder_path = r"C:\Users\Mohammed.Hashem\OneDrive - Arup\EG" #complete path eg. "C:\Users\XXXXX\Desktop\folder_name"
# file_to_check = "282442-ADC-DE-PWD-DWG-CIV1-09300.pdf"     #just the file name eg. "filenames" 
# comparison_list_output_file_name = "duplicate_comparison" #output_file_name

#Output is an excel sheet where each column represent duplicate files

#Mohammed Hashem - 2024-03-27

########################################################################
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox, Text
from pathlib import Path
from PyPDF2 import PdfReader
import csv
import shutil

def find_files_with_same_name(parent_folder, filename):
    """
    Find files with the same name within a given parent folder.

    Args:
        parent_folder (str): The path to the parent folder.
        filename (str): The filename to search for.

    Returns:
        list: A list of paths to files with the specified filename.
    """
    parent_path = Path(parent_folder)
    file_paths = []
    
    # Iterate over all subfolders and files
    for current_path in parent_path.glob('**/*'):
        if current_path.is_file() and current_path.stem == filename and current_path.suffix == ".pdf":
            file_paths.append(current_path)
    return file_paths

def generate_pckg_short_name(original_name):
    parts = original_name.split('-')
    txt_1 = parts[-2]
    txt_2 = parts[-3]
    txt_3 = parts[-6]
    rev = parts[-1]
    pckg_short_name =  f"Pkg {txt_3}-{txt_1}-{txt_2} Rev {rev}"
    return pckg_short_name



def copy_and_rename_files(file_paths_list, parent_folder, file_to_check):
    """
    Copy files from a list to a new folder and rename them with a specific suffix.

    Args:
        file_paths_list (list): A list of paths to the files to be copied.
        parent_folder (str): The path to the parent folder.
        file_to_check (str): The filename used for creating the destination folder and renaming files.

    Returns:
        str: The path to the destination folder where files are copied.
    """
    parent_path = Path(parent_folder)
    destination_folder = parent_path / f"{file_to_check} - duplicate check"
    
    # Create the destination folder if it doesn't exist
    destination_folder.mkdir(parents=True, exist_ok=True)
    
    # Copy and rename files
    for current_path in file_paths_list:
        # Get the first parent folder name
        first_parent_folder = current_path.parents[0].name
        
        pckg_suffix =  generate_pckg_short_name(first_parent_folder)
        # print(f"{pckg_suffix=}")



        # Construct the new filename with suffix
        new_filename = f"{current_path.stem}_{pckg_suffix}{current_path.suffix}"
        # print(f"{new_filename=}")
        # Destination path with new filename
        destination_file_path = destination_folder / new_filename
        
        # Copy the file and rename it
        shutil.copy(current_path, destination_file_path)

    return destination_folder

def compare_pdfs(pdf1, pdf2):
    """
    Compare the content of two PDF files.

    Args:
        pdf1 (str): The path to the first PDF file.
        pdf2 (str): The path to the second PDF file.

    Returns:
        bool: True if the content of the PDF files is identical, False otherwise.
    """
    # Open the PDF files
    with open(pdf1, 'rb') as file1, open(pdf2, 'rb') as file2:
        # Create PdfFileReader objects
        reader1 = PdfReader(file1)
        reader2 = PdfReader(file2)

        # Check the number of pages
        if len(reader1.pages) != len(reader2.pages):
            return False

        # Check each page's content
        for page_num in range(len(reader1.pages)):
            page1_text = reader1.pages[page_num].extract_text()
            page2_text = reader2.pages[page_num].extract_text()
            if page1_text != page2_text:
                return False

    return True

def check_duplicate_pdfs(folder_path):
    """
    Check for duplicate PDF files within a folder based on their content.

    Args:
        folder_path (str): The path to the folder containing PDF files.

    Returns:
        list: A list of lists containing filenames of duplicate PDF files.
    """
    duplicates = []

    # Iterate over PDF files in the folder
    pdf_files = list(Path(folder_path).glob('*.pdf'))
   
    
    while pdf_files:
        current_pdf = pdf_files.pop(0)
        
        
        current_duplicates = [current_pdf.name]

        for pdf_file in pdf_files[:]:
            
            if compare_pdfs(str(current_pdf), str(pdf_file)):
                current_duplicates.append(pdf_file.name)
                pdf_files.remove(pdf_file)

        if len(current_duplicates) > 1:
            duplicates.append(current_duplicates)

    return duplicates

def write_csv_from_list_of_lists(list_of_lists, output_folder, output_filename):
    """
    Write a list of lists to a CSV file.

    Args:
        list_of_lists (list): A list of lists to be written to the CSV file.
        output_folder (str): The path to the folder where the CSV file will be saved.
        output_filename (str): The name of the CSV file (without file extension).
    """
    if not list_of_lists:
        print("No Duplicates")
        return  # Return if the list is empty
    output_path = Path(output_folder) / (output_filename + '.csv')
    # Find the length of the longest inner list
    max_length = max(len(inner_list) for inner_list in list_of_lists)
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write each inner list as a column
        for i in range(max_length):
            row = [inner_list[i] if i < len(inner_list) else '' for inner_list in list_of_lists]
            writer.writerow(row)


# if "." in file_to_check:
#     file_to_check = file_to_check.split(".")[0]
# if "." in comparison_list_output_file_name:
#     comparison_list_output_file_name = comparison_list_output_file_name.split(".")[0]


# # Find files with the same name as 'file_to_check' within 'folder_path'
# path_list = find_files_with_same_name(folder_path, file_to_check)

# # Copy and rename files from 'path_list' to a new folder
# destination_folder = copy_and_rename_files(path_list, folder_path, file_to_check)

# # Check for duplicate PDF files within 'destination_folder'
# dupes = check_duplicate_pdfs(destination_folder)

# # Write the list of lists containing duplicate filenames to a CSV file
# write_csv_from_list_of_lists(dupes, destination_folder, comparison_list_output_file_name)

def browse_folder_path():
    folder_path = filedialog.askdirectory()
    folder_path_entry.delete(0, 'end')
    folder_path_entry.insert(0, folder_path)

def browse_file_to_check():
    file_to_check = filedialog.askopenfilename()
    if file_to_check:  # Check if a file was selected
        # Extract just the filename
        file_to_check = Path(file_to_check).name
        file_to_check_entry.delete(0, 'end')
        file_to_check_entry.insert(0, file_to_check)


root = Tk()
root.title("PDF Duplicate Checker")

# Explanation labels with left alignment
Label(root, text="Folder Path:", anchor="w").grid(row=0, column=0, sticky="w")
Label(root, text="Select the folder containing PDF files to check for duplicates.", anchor="w").grid(row=0, column=3, sticky="w")
Label(root, text="File to Check:", anchor="w").grid(row=1, column=0, sticky="w")
Label(root, text="Select the PDF file you want to check for duplicates.", anchor="w").grid(row=1, column=3, sticky="w")

# Entry fields
folder_path_entry = Entry(root, width=50)
folder_path_entry.grid(row=0, column=1)
Button(root, text="Browse", command=browse_folder_path).grid(row=0, column=2)

file_to_check_entry = Entry(root, width=50)
file_to_check_entry.grid(row=1, column=1)
Button(root, text="Browse", command=browse_file_to_check).grid(row=1, column=2)

# Text widget for output
output_text = Text(root, height=10, width=50)
output_text.grid(row=3, columnspan=3)

# Function to write output to the text widget
def write_output_to_text(text):
    output_text.insert("end", text + "\n")
    output_text.see("end")  # Scroll to the end

# Function to execute the script
def execute_script():
    folder_path = folder_path_entry.get()
    file_to_check = file_to_check_entry.get()

    # Remove file extension if present
    if "." in file_to_check:
        file_to_check = file_to_check.split(".")[0]

    path_list = find_files_with_same_name(folder_path, file_to_check)
    destination_folder = copy_and_rename_files(path_list, folder_path, file_to_check)
    dupes = check_duplicate_pdfs(destination_folder)

    if not dupes:
        write_output_to_text("No Duplicates")
        return

    # If all instances of the file name are duplicates
    if len(dupes) == 1 and len(dupes[0]) == len(path_list):
        write_output_to_text("All instances of this file name are duplicates")

    # Generate package short name based on the file to check
    pckg_short_name = generate_pckg_short_name(file_to_check)

    # Fixed output filename with pckg_short_name appended
    output_filename = "duplicate_comparison_" + pckg_short_name

    write_csv_from_list_of_lists(dupes, destination_folder, output_filename)
    write_output_to_text("Duplicate comparison file written successfully.")

# Button to execute script
Button(root, text="Execute", command=execute_script).grid(row=4, columnspan=3)

root.mainloop()