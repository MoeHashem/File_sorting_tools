####
#UPDATE PATH BELOW TO WORKING LOCATION !!
#CREATE _Others AND ALL OTHER STRUCTURE FILES FIRST
####

import os

path = r"C:\Users\Mohammed.Hashem\OneDrive - Arup\Projects\07 - On-Corr\DMRP Reviews\Woodbine"

type_filter = [".pdf", ".py", ".txt"]
folders = []
disciplines = ["CRD Highways", "CTR Traffic", "CWM Drainage", "STR Structural", "ENV Environmental", "LND Landscape", "PTY Property", "UTL Utilities", "MEC Mechanical", "ELE Electrical", "ART Architectural", "CCC Cable Containment", "CEG Civil Layout", "GBN Grounding", "PTY Property", "CIV Civil", "GEO Geotech"]
for folder in os.listdir(path): #detects all the folders (not pdf, txt, etc)
    if not any(folder.__contains__(x) for x in type_filter):
        folders.append(folder) 
        



all_files = [file for file in os.listdir(path)] #makes sure only desired file types are being looped through (pdf)
files = set(all_files) - set(folders)


for file in files:#check every file
    folder_count=0
    src = os.path.join(path, file)
    file_folder = "_Others"
    for folder in folders: #checks if filename has any or multiple of the structures(folders) in submission
        if folder in file:
            file_folder = folder
            folder_count = folder_count +1

    file_disp = "_Others"
    for displine in disciplines: ##checks if filename has any of the disciplines
        if displine[:3] in file:
            file_disp = displine

    if folder_count>1:
        dest = os.path.join(path, "_Others", file) #if this pdf is relevant to multiple structures, send to Others
    else:
        if file_folder == "_Others":
            dest = os.path.join(path, file_folder, file) #if file is not relevant to any specific submisison, send to others
        else:
            dest = os.path.join(path, file_folder, file_disp, file) #if file is relevent to a specific discipline in a specific folder, send it there
            if not os.path.exists(os.path.join(path, file_folder, file_disp)):# creates discipline folders if not present
                os.makedirs(os.path.join(path, file_folder, file_disp))

    os.rename(src, dest) #moves files






# for file in files:#check every file
#     src = os.path.join(path, file)
#     for folder in folders:#check every folder (structure)
#         print(folder)
#         print(file)
#         print(folder in file)
#         if folder in file:#if folder/structure name is in the file name
#             for disp in disciplines:
#                 if disp in file:#selects correct disp folder based on shorthand
#                     for x in os.listdir(os.path.join(path, folder)):
#                         if disp in x:
#                             d_folder = x
#                 else:
#                     d_folder = "_Others2"
#                 dest = os.path.join(path, folder, d_folder, file)
                
#         else: #if structure does not exist sent to others
#             dest = os.path.join(path, "_Others", file)
#     os.rename(src, dest)


# files = [file for file in os.listdir(path) if file not in folders]
# for file in files:
#     for folder in folders:
#         if folder in file:
#             for disp in disciplines:
#                 if disp in file:
#                     for x in folders:
#                         if disp in x:
#                             d_folder = x
#                         else:
#                             d_folder = "_Others2"
#                     d_folder = folders
#                     src = os.path.join(path, file)
#                     dest = os.path.join(path, folder, d_folder, file)
#                     os.rename(src, dest)
#         else:
#             src = os.path.join(path, file)
#             dest = os.path.join(path, "_Others", file)
#             os.rename(src, dest)



#src = os.path.join(path, filename)
#dest = os.path.join(path, "BridgeAA", filename)




#os.rename(src, dest)