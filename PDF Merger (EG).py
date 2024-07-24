    # This script processes PDF files in a specified folder with names in the format:
    # 282442-ADC-DES0-XXX-DWG-YYY-ZZZZZ.pdf
    # The files are sorted by the XXX, YYY, and ZZZZZ parts of their names. PDFs with the same XXX are merged into
    # a single PDF with a name in the format: Pckg1/2/3/4_60%_{XXX}_combined.pdf. The package number is determined
    # by the presence of 'A', 'B', 'C', or 'D' in a specific location of the folder name (e.g., 2024-07-15 s-104*D*-DES-OOOO-001-001 -A).
    
#New users use pip install pypdf
#Run the code and input file path to target folder when prompted

import os
import re
from pypdf import PdfWriter
from tqdm import tqdm

def get_package_number(folder_name):
    """
    Determines the package number based on the character 'A', 'B', 'C', or 'D'
    found at a specific position in the folder name.
    """
    # Extract the character at the specific position, case-insensitive
    match = re.search(r'\d{4}-\d{2}-\d{2} s-\d{3}([ABCD])-', folder_name, re.IGNORECASE)
    if match:
        char = match.group(1).upper()
        if char == 'A':
            return 1
        elif char == 'B':
            return 2
        elif char == 'C':
            return 3
        elif char == 'D':
            return 4
    raise ValueError("Folder name does not contain A/B/C/D at the specified location.")

def delete_existing_merged_files(folder_path):
    """
    Deletes existing merged PDF files in the specified folder.
    """
    for file_name in os.listdir(folder_path):
        if "combined" in file_name.lower() and file_name.endswith(".pdf"):
            try:
                os.remove(os.path.join(folder_path, file_name))
                print(f"Deleted existing file: {file_name}")
            except Exception as e:
                print(f"Failed to delete file {file_name}: {e}")

def sort_files(file_list):
    """
    Sorts the PDF files by the XXX, YYY, and ZZZZZ parts of the file name.
    """
    def sort_key(file_name):
        parts = file_name.split('-')
        if len(parts) < 7 or not parts[3].isalnum():
            raise ValueError(f"File name {file_name} does not match the expected format.")
        return (parts[3], parts[5], parts[6].split('.')[0])

    return sorted(file_list, key=sort_key)

def merge_pdfs_by_xxx(file_list, package_number, output_dir):
    """
    Merges PDFs with the same XXX into a single PDF and saves it with the specified naming format.
    """
    merged_files = {}
    for file in file_list:
        parts = file.split('-')
        if len(parts) < 7 or not parts[3].isalnum():
            print(f"Skipping file with incorrect format: {file}")
            continue
        xxx = parts[3]
        if xxx not in merged_files:
            merged_files[xxx] = []
        merged_files[xxx].append(file)

    # Initialize tqdm progress bar
    progress = tqdm(total=len(merged_files.items()), desc='Merging PDFs', unit='file')

    for xxx, files in merged_files.items():
        writer = PdfWriter()
        for file in files:
            writer.append(os.path.join(output_dir, file))
        output_filename = f"Pckg{package_number}_60%_{xxx}_combined.pdf"
        output_path = os.path.join(output_dir, output_filename)

        # Write the merged PDF
        with open(output_path, "wb") as output_pdf:
            writer.write(output_pdf)
        progress.update(1)  # Update progress bar
    progress.close()

def main():
    
  
    # User input for the folder path
    folder_path = input("Please enter the path to the folder containing the PDF files: ")
    
    if not os.path.isdir(folder_path):
        print(f"The path {folder_path} is not a valid directory.")
        return

    # Delete existing merged files before starting any operations
    print("Deleting existing merged PDF files...")
    delete_existing_merged_files(folder_path)

    folder_name = os.path.basename(folder_path)
    try:
        package_number = get_package_number(folder_name)
    except ValueError as e:
        print(e)
        return

    # Filter only PDF files that match the expected format
    pattern = re.compile(r'282442-ADC-DES0-[A-Z0-9]{3}-DWG-[A-Z0-9]{4}-\d{5}\.pdf', re.IGNORECASE)
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf') and pattern.match(f)]

    if not pdf_files:
        print(f"No PDF files matching the expected format found in {folder_path}. Exiting.")
        return

    try:
        sorted_files = sort_files(pdf_files)
    except ValueError as e:
        print(e)
        return

    merge_pdfs_by_xxx(sorted_files, package_number, folder_path)

if __name__ == "__main__":
    main()
