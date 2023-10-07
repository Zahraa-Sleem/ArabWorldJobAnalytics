import os
import json

def add_job_role(folder_name):
    # Specify the directory path you want to list files from
    directory_path = folder_name

    # Use the os.listdir() function to get a list of all files and directories in the specified directory
    all_files_and_directories = os.listdir(directory_path)
    
    for file in all_files_and_directories:
            print(file)
            with open(folder_name+"/"+file, "r",encoding='utf-8') as json_file:
                object=json.load(json_file)
            if  "Job Role" not in  object["Data"].keys():
                object["Data"]["Job Role"]="Unspecified"
                with open(folder_name+"/"+file, "w",encoding='utf-8') as json_file:
                    json.dump(object)
                        
    

add_job_role("data_store")
                    
