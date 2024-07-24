###
# This script processes PDF and CAD files in a specified folder and its subfolders.

# 1. **Finding Duplicate PDFs**:
#    - The script generates MD5 hashes for each PDF file in the folder.
#    - It identifies and lists duplicate PDFs, grouping them together in columns in a CSV file.
#    - The output CSV file is named "PDF Duplicate check.csv" and is saved in the same folder.
#    - Each file is named in the format: `Pckg_{Package Number}_{Filename}`, where the package number is determined by the character 'A', 'B', 'C', or 'D' in a specific position in the folder name. For example, if the folder name contains `2024-07-15 s-104B-DES-OOOO-001-001`, the package number would be `2` (for 'B').

# 2. **Comparing PDFs and CADs**:
#    - The script compares PDF and CAD files based on their names.
#    - It identifies:
#      - PDF files with no corresponding CAD files.
#      - CAD files with no corresponding PDF files.
#      - Matching PDF and CAD files.
#    - The results are saved in a CSV file named "CAD_PDF check.csv" with three columns:
#      - PDF files with no CAD counterpart
#      - CAD files with no PDF counterpart
#      - Matching PDF and CAD files

# **Usage**:
# 1. Ensure you have the required libraries installed:
#    pip install pypdf tqdm

# 2. Run the script and input the entire folder path to the parent folder when prompted (eg. C:\Users\Mohammed.Hashem\Desktop\Folder\)
###

import os
import re
from pathlib import Path
import hashlib
import csv
from tqdm import tqdm
from itertools import zip_longest

def find_files_by_extension(folder_path, extensions):
    """
    Find all files with the specified extensions in a given folder and its subfolders.

    Args:
        folder_path (str): The path to the folder.
        extensions (tuple): A tuple of file extensions to search for.

    Returns:
        list: A list of paths to files with the specified extensions.
    """
    files = []
    for extension in extensions:
        files.extend(Path(folder_path).glob(f'**/*{extension}'))
    return files

def hash_file(file_path):
    """
    Generate an MD5 hash for a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The MD5 hash of the file.
    """
    md5_hash = hashlib.md5()
    with open(file_path, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
    return md5_hash.hexdigest()

def find_duplicates(pdf_files):
    """
    Find duplicate PDF files by comparing their MD5 hash values.

    Args:
        pdf_files (list): A list of paths to PDF files.

    Returns:
        list: A list of lists containing paths of duplicate PDF files.
    """
    checked_files = set()
    duplicates = []

    for i, current_pdf in enumerate(tqdm(pdf_files, desc="Checking for duplicates")):
        if current_pdf in checked_files:
            continue

        current_hash = hash_file(current_pdf)
        current_duplicates = [current_pdf]

        for other_pdf in pdf_files[i+1:]:
            if other_pdf not in checked_files:
                other_hash = hash_file(other_pdf)
                if current_hash == other_hash:
                    current_duplicates.append(other_pdf)
                    checked_files.add(other_pdf)

        if len(current_duplicates) > 1:
            duplicates.append(current_duplicates)
            checked_files.update(current_duplicates)

    return duplicates

def write_csv(data, output_path, headers=None):
    """
    Write data to a CSV file.

    Args:
        data (list): A list of rows to be written to the CSV file.
        output_path (str): The path to the CSV file to be created.
        headers (list): Optional list of column headers for the CSV file.
    """
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if headers:
            writer.writerow(headers)
        writer.writerows(data)

def get_package_number(folder_name):
    """
    Determines the package number based on the character 'A', 'B', 'C', or 'D'
    found at a specific position in the folder name.
    """
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
    return 0

def find_mismatched_files(pdf_files, cad_files):
    """
    Find PDF files with no CAD counterpart and CAD files with no PDF counterpart.

    Args:
        pdf_files (list): A list of paths to PDF files.
        cad_files (list): A list of paths to CAD files.

    Returns:
        tuple: Three lists containing paths of PDFs with no CAD counterpart, CADs with no PDF counterpart, and matching files.
    """
    pdf_basenames = {pdf.stem: pdf for pdf in pdf_files}
    cad_basenames = {cad.stem: cad for cad in cad_files}

    pdf_no_cad = [pdf for basename, pdf in pdf_basenames.items() if basename not in cad_basenames]
    cad_no_pdf = [cad for basename, cad in cad_basenames.items() if basename not in pdf_basenames]
    matching_files = [pdf for basename, pdf in pdf_basenames.items() if basename in cad_basenames]

    return pdf_no_cad, cad_no_pdf, matching_files

def main(folder_path):
    pdf_files = find_files_by_extension(folder_path, ('.pdf',))
    cad_files = find_files_by_extension(folder_path, ('.dwg', '.dxf', '.dgn'))  # Assuming CAD files have these extensions

    # Show a progress bar for PDF comparison
    duplicates = find_duplicates(pdf_files)
        
    if duplicates:
        output_path = Path(folder_path) / "PDF Duplicate check.csv"
        formatted_duplicates = []
        
        for duplicate_set in duplicates:
            formatted_set = []
            for file_path in duplicate_set:
                parent_folder_name = Path(file_path).parent.name
                package_number = get_package_number(parent_folder_name)
                formatted_filename = f"Pckg_{package_number}_{Path(file_path).name}"
                formatted_set.append(formatted_filename)
            formatted_duplicates.append(formatted_set)
        
        # Transpose the list to make duplicates columns instead of rows
        max_length = max(len(dup_set) for dup_set in formatted_duplicates)
        transposed_data = list(zip_longest(*formatted_duplicates, fillvalue=''))
        
        # Create headers based on the maximum number of duplicates found
        headers = [f"Duplicates {i+1}" for i in range(max_length)]
        
        write_csv(transposed_data, output_path, headers=headers)
        print(f"Duplicate PDFs have been listed in {output_path}")
    else:
        print("No duplicate files found, no output file created.")

    # Show a progress bar for CAD/PDF comparison
    pdf_no_cad, cad_no_pdf, matching_files = find_mismatched_files(pdf_files, cad_files)

    if pdf_no_cad or cad_no_pdf or matching_files:
        output_path = Path(folder_path) / "CAD_PDF check.csv"
        formatted_no_cad = [pdf.name for pdf in pdf_no_cad]
        formatted_no_pdf = [cad.name for cad in cad_no_pdf]
        formatted_matching_files = [file.name for file in matching_files]

        data = list(zip_longest(formatted_no_cad, formatted_no_pdf, formatted_matching_files, fillvalue=''))
        write_csv(data, output_path, headers=["PDF with no CAD", "CAD with no PDF", "Matching CAD and PDF"])
        print(f"CAD/PDF mismatches and matches have been listed in {output_path}")
    else:
        print("No CAD/PDF mismatches or matches found, no output file created.")

if __name__ == "__main__":
    folder_path = input("Enter the folder path containing PDF and CAD files: ")
    main(folder_path)
