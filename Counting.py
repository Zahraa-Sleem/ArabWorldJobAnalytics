import os
import json
from collections import Counter

def load_scraped_data(folder_name):
    
    # Specify the directory path you want to list files from
    directory_path = folder_name

    # Use the os.listdir() function to get a list of all files and directories in the specified directory
    all_files_and_directories = os.listdir(directory_path)
    
    jobs=[]
    
    for file in all_files_and_directories:
            with open(folder_name+"/"+file, "r",encoding='utf-8') as json_file:
                jobs.append(json.load(json_file)["Data"]["Job Role"]) 
    
    return jobs

def count_titles(data):

    frequency_counter = Counter(data)

    frequency_dict = dict(frequency_counter)

    return frequency_dict
       
 
titles=load_scraped_data("data_store")
print(len([lm for lm in titles if lm=="Unspecified"]))
