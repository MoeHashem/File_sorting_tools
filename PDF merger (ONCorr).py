####
#UPDATE PATH BELOW TO WORKING LOCATION !!
####

import os
#pip install PyPDF2 
from PyPDF2 import PdfReader, PdfWriter, PdfMerger



path = r"C:\Users\Mohammed.Hashem\OneDrive - Arup\Projects\07 - On-Corr\DMRP Reviews\\Woodbine"

all_folders = [] #gives entire path names for main and sub folders
for root, dirs, files in os.walk(path):
  for name in dirs:
    all_folders.append(os.path.join(root, name))

main_folders = []
type_filter = [".pdf", ".py", ".txt"]
for folder in os.listdir(path): #detects all the folders in main directory(not pdf, txt, etc)
    if not any(folder.__contains__(x) for x in type_filter):
        main_folders.append(folder) 

sub_folders = all_folders[len(main_folders):]


for sub_folder in sub_folders:
    head, tail = os.path.split(sub_folder)
    if tail == "_Others":
        continue
    structure_name = sub_folder.split(f"\\")[-2]
    files_to_merge = os.listdir(sub_folder)#all files in subfolder
    
    merged_name = ("COMBINED_" + structure_name + "_" + tail[4:] + ".pdf").upper()
    
    if not os.path.exists(merged_name):#creates new merged document if one doesnt already exist
        merger = PdfMerger()
        for pdf in files_to_merge:
            merger.append(open(os.path.join(sub_folder, pdf), 'rb'))
    
        with open(f"{os.path.join(sub_folder, merged_name)}","wb") as fout:
            merger.write(fout)




