####
#UPDATE INPUTS BELOW AS NEEDED !!
#First time users: type "pip install PyPDF2" and "pip install pandas" in the terminal below (VSCode) or in the comand prompt if using Notepad
####

import os
from PyPDF2 import PdfMerger
import zipfile
import pandas as pd
import csv

###INPUTS####
folder_path = r"C:\Users\Mohammed.Hashem\Desktop\test" #complete path eg. "C:\Users\XXXXX\Desktop\folder_name"
txt_file_name = "File_Names.txt"     #just the file name eg. "filenames.txt"
table_file_name = "CAD_PDF_Check.txt"   #name of the table file (change to .csv if you want excel table, txt for quick and dirty view - recommended)
file_types_to_track = ["pdf", "dwg"]


def get_merged_file_name(folder_path):
    """
    For folder name S-103A-GEN-0000-00Y-00X-Z, it would be "Pkg X-Y Rev Z.pdf"
    """
    folder_name = os.path.basename(folder_path)
    parts = folder_name.split('-')
    txt_1 = parts[-2]
    txt_2 = parts[-3]
    txt_3 = parts[-6]
    rev = parts[-1]
    pckg_short =  f"Pkg {txt_3}-{txt_1}-{txt_2} Rev {rev}"
    return pckg_short


def list_tracked_files_in_folder(folder_path, file_types_to_track):
    """
    Lists all .pdf files in a folder, sorted by second to last set of digits, then last set 
    """
    tracked_files = []
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            for suffix in file_types_to_track:
                if file_name.lower().endswith(suffix):
                    tracked_files.append((file_name))
        tracked_files.sort(key=lambda x: (x.split('.')[-1], x.split('-')[-2], x.split('-')[-1].split('.')[0]))
    return tracked_files


def write_list_to_txt(file_names, output_file, folder_path):
    """
    Prints list to .txt
    """
    output_path = os.path.join(folder_path, output_file)
    with open(output_path, 'w') as f:
        for file_name in file_names:
            f.write(file_name + '\n')


def merge_pdfs_with_marker(file_list, marker, merged_file_name, folder_path):
    merger = PdfMerger()
    
    for file_name in file_list:
        if marker.lower() in file_name.lower() and ".pdf" in file_name:
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'rb') as file:
                merger.append(file)
    
    merged_file_path = os.path.join(folder_path, merged_file_name)
    with open(merged_file_path, 'wb') as output_file:
        merger.write(output_file)


def unzip_zip_files(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith('.zip'):
            zip_file_path = os.path.join(folder_path, file_name)
            destination_folder = os.path.join(folder_path, os.path.splitext(file_name)[0])
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(destination_folder)


def unique_file_df(file_list, marker):
    list_of_files = []
    list_of_pdfs = []
    list_of_cads = []
    for file_name in file_list:
        if marker.lower() in file_name.lower():
            stripped_name = file_name.split(".")[0]
            list_of_files.append(stripped_name)
            if file_name.lower().endswith(".pdf"):
                list_of_pdfs.append(stripped_name)
            elif file_name.lower().endswith(".dwg"):
                list_of_cads.append(stripped_name)

    list_of_files = list(set(list_of_files))
    list_of_files.sort(key=lambda x: (x.split('-')[-2], x.split('-')[-1]))

    # Create DataFrame
    data = {'PDF': [file_name in list_of_pdfs for file_name in list_of_files],
            'CAD': [file_name in list_of_cads for file_name in list_of_files]}
    df = pd.DataFrame(data, index=list_of_files)
    
    # Add new column 'Both Formats'
    df['Both Formats OK'] = df['PDF'] & df['CAD']
    
    # Sort DataFrame
    # df['Suffix'] = df.index.map(lambda x: x.split('.')[-1])
    # df['SecondToLast'] = df.index.map(lambda x: x.split('-')[-2])
    # df['Last'] = df.index.map(lambda x: x.split('-')[-1].split('.')[0])
    #df = df.sort_values(by=['Suffix', 'SecondToLast', 'Last'])
    # df = df.drop(columns=['Suffix', 'SecondToLast', 'Last'])
    
    df.index.name = "x" * len(stripped_name)

    return df

def print_df_to_csv(df, table_file_name, folder_path):
    
    output_path = os.path.join(folder_path, table_file_name)
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow(df.columns)  # Write column headers
        for index, row in df.iterrows():
            writer.writerow([index] + row.tolist())

def print_df_to_txt(df, table_file_name, folder_path):
    # Print DataFrame to tab-separated text file
    output_path = os.path.join(folder_path, table_file_name)
    with open(output_path, 'w') as file:
        file.write(df.to_csv(sep='\t'))





unzip_zip_files(folder_path) #unzips the CAD files
file_names = list_tracked_files_in_folder(folder_path, file_types_to_track) #all files .pdf or .dwg
write_list_to_txt(file_names, txt_file_name, folder_path) #prints all the tracked file names to a txt file
merged_file_name = get_merged_file_name(folder_path) # determines merged file name based on package name
merge_pdfs_with_marker(file_names, "DWG", merged_file_name, folder_path) #merges all DWG.pdfs (in order)
df = unique_file_df(file_names, "DWG") #creates table of CAD and PDF comparison
if table_file_name.endswith(".txt"):
    print_df_to_txt(df, table_file_name, folder_path)
else:
    print_df_to_csv(df, table_file_name, folder_path)



