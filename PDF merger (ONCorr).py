####
#UPDATE PATH BELOW TO WORKING LOCATION !!
#pip install pypdf
####



path = r"C:\Users\Mohammed.Hashem\OneDrive - Arup\06-Corridor Submissions\LSW Cordr Pck A 240624"
import os
from pypdf import PdfReader, PdfWriter


# Collect all folder paths
all_folders = []
for root, dirs, files in os.walk(path):
    for name in dirs:
        all_folders.append(os.path.join(root, name))

# Filter main folders
main_folders = []
type_filter = [".pdf", ".py", ".txt"]
for folder in os.listdir(path):
    if not any(folder.endswith(x) for x in type_filter):
        main_folders.append(folder)

# Collect sub-folder paths
sub_folders = all_folders[len(main_folders):]

# Iterate over sub-folders and merge PDFs
for sub_folder in sub_folders:
    head, tail = os.path.split(sub_folder)
    if tail == "_Others":
        print(f"Skipping folder: {sub_folder}")
        continue
    
    structure_name = sub_folder.split(f"\\")[-2]
    files_to_merge = os.listdir(sub_folder)
    
    merged_name = ("COMBINED_" + structure_name + "_" + tail[4:] + ".pdf").upper()
    merged_path = os.path.join(sub_folder, merged_name)
    
    if not os.path.exists(merged_path):
        # print(f"Creating merged PDF: {merged_path}")
        writer = PdfWriter()
        
        for pdf in files_to_merge:
            if pdf.lower().endswith('.pdf'):
                pdf_path = os.path.join(sub_folder, pdf)
                try:
                    # print(f"Appending file: {pdf_path}")
                    reader = PdfReader(pdf_path)
                    for page_num in range(len(reader.pages)):
                        writer.add_page(reader.pages[page_num])
                except Exception as e:
                    print(f"Failed to append {pdf_path}: {e}")
            else:
                print(f"Skipping non-PDF file: {pdf}")

        try:
            with open(merged_path, "wb") as fout:
                writer.write(fout)
            # print(f"Successfully created merged PDF: {merged_path}")
        except Exception as e:
            print(f"Failed to write merged PDF {merged_path}: {e}")
    else:
        print(f"Merged PDF already exists: {merged_path}")



# import os
# #pip install PyPDF2 
# from PyPDF2 import PdfReader, PdfWriter, PdfMerger



# path = r"C:\Users\Mohammed.Hashem\OneDrive - Arup\Projects\07 - On-Corr\DMRP Reviews\\Woodbine"

# all_folders = [] #gives entire path names for main and sub folders
# for root, dirs, files in os.walk(path):
#   for name in dirs:
#     all_folders.append(os.path.join(root, name))

# main_folders = []
# type_filter = [".pdf", ".py", ".txt"]
# for folder in os.listdir(path): #detects all the folders in main directory(not pdf, txt, etc)
#     if not any(folder.__contains__(x) for x in type_filter):
#         main_folders.append(folder) 

# sub_folders = all_folders[len(main_folders):]


# for sub_folder in sub_folders:
#     head, tail = os.path.split(sub_folder)
#     if tail == "_Others":
#         continue
#     structure_name = sub_folder.split(f"\\")[-2]
#     files_to_merge = os.listdir(sub_folder)#all files in subfolder
    
#     merged_name = ("COMBINED_" + structure_name + "_" + tail[4:] + ".pdf").upper()
    
#     if not os.path.exists(merged_name):#creates new merged document if one doesnt already exist
#         merger = PdfMerger()
#         for pdf in files_to_merge:
#             merger.append(open(os.path.join(sub_folder, pdf), 'rb'))
    
#         with open(f"{os.path.join(sub_folder, merged_name)}","wb") as fout:
#             merger.write(fout)




# import os
# # pip install pypdf
# from pypdf import PdfReader, PdfWriter, PdfMerger

# path = r"C:\Users\Mohammed.Hashem\OneDrive - Arup\Projects\07 - On-Corr\11 - LSW Submission Review\06-Corridor Submissions\LSW Cordr Pck A 240624"

# all_folders = []  # gives entire path names for main and sub folders
# for root, dirs, files in os.walk(path):
#     for name in dirs:
#         all_folders.append(os.path.join(root, name))

# main_folders = []
# type_filter = [".pdf", ".py", ".txt"]
# for folder in os.listdir(path):  # detects all the folders in main directory (not pdf, txt, etc)
#     if not any(folder.__contains__(x) for x in type_filter):
#         main_folders.append(folder)

# sub_folders = all_folders[len(main_folders):]

# for sub_folder in sub_folders:
#     head, tail = os.path.split(sub_folder)
#     if tail == "_Others":
#         continue
#     structure_name = sub_folder.split(f"\\")[-2]
#     files_to_merge = os.listdir(sub_folder)  # all files in subfolder

#     merged_name = ("COMBINED_" + structure_name + "_" + tail[4:] + ".pdf").upper()

#     if not os.path.exists(merged_name):  # creates new merged document if one doesn't already exist
#         merger = PdfMerger()
#         for pdf in files_to_merge:
#             merger.append(os.path.join(sub_folder, pdf))
    
#         with open(f"{os.path.join(sub_folder, merged_name)}", "wb") as fout:
#             merger.write(fout)