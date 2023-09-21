import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

def get_scraped_ids(folder_name):
    
    # Specify the directory path you want to list files from
    directory_path = folder_name

    # Use the os.listdir() function to get a list of all files and directories in the specified directory
    all_files_and_directories = os.listdir(directory_path)
    
    # Iterate through the list and filter out only the files (excluding directories)
    ids = [file.split('.')[0] for file in all_files_and_directories if os.path.isfile(os.path.join(directory_path, file))]

    return ids


def get_element_by_xpath(driver,xpath):
    while True:
            try:
                # Find the starting point for job description
                obj = driver.find_element(By.XPATH, xpath)
                return obj
            except Exception as e:
                time.sleep(1)
                # print(f"Error: {e}")
                pass

def get_job_info(driver, job_id):
    
    print("Opened page",job_id)
    # Getting the URL
    job_url = f'https://www.bayt.com/en/international/jobs/?jobId={job_id}'
    driver.get(job_url)
    
    job_description = ""  # Initialize the job description string
    skills = []  # Initialize the skills list
    skills_start="Not found"
    
    if "Job Details" in get_element_by_xpath(driver,'//*[@id="view_inner"]/div/div[2]/h2[2]').text:
        print("Job Description is h2[1]")
        job_description_start=get_element_by_xpath(driver,'//*[@id="view_inner"]/div/div[2]/h2[1]')
    else:
        print("Job Description is h2[2]")
        job_description_start=get_element_by_xpath(driver,'//*[@id="view_inner"]/div/div[2]/h2[2]')
        
    # Iterate through siblings
    current_element = job_description_start.find_element(By.XPATH, "./following-sibling::*")
    while current_element is not None:
        job_description += current_element.text
        
        if current_element.tag_name == "h2" and "Skills" in current_element.text:
            print("Job Description",job_description)
            skills_start = current_element
            print("Skills Start",skills_start)
            break
        elif current_element.tag_name == "h2" and "Job Details" in current_element.text:
            print("Job Description",job_description)
            print("Skills Start",skills_start)
            break
        
        # Move to the next sibling
        current_element = current_element.find_element(By.XPATH, "./following-sibling::*")
    
    if skills_start!="Not found":
        # Iterate through siblings starting from the "Skills" section
        current_element = skills_start.find_element(By.XPATH, "./following-sibling::*")
        while current_element is not None:
            # Check if we've reached the "Job Details" section
            if current_element.tag_name=="h2" and "Job Details" in current_element.text:
                print("Skills",skills)
                break
            elif(current_element.text != ""):
                skills.append(current_element.text)
            
            current_element = current_element.find_element(By.XPATH, "./following-sibling::*")


    parent_element_details=get_element_by_xpath(driver,'//*[@id="view_inner"]/div/div[2]/dl[1]')
     
    # Find child elements within the <dl> element
    child_elements_details = parent_element_details.find_elements(By.XPATH, ".//*")
    
    # Create a dictionary to store the extracted information concerning details
    info_dict_general = {}
    
    for child in child_elements_details:
        try:
            # Extract the <dt> and <dd> elements
            dt_element = child.find_element(By.TAG_NAME, "dt")
            dd_element = child.find_element(By.TAG_NAME, "dd")

            # Get the text content of <dt> and <dd> elements and add it to the dictionary
            info_dict_general[dt_element.text] = dd_element.text
        except:
            pass
    
    print("Info Dict General",info_dict_general)
    
    parent_element_preffered=False
    info_dict_preffered = {}
    preferred=False
    
    try:
        #Check if preferred candidate details are found
        preferred=parent_element_details.find_element(By.XPATH, "./following-sibling::*").tag_name=="h2" and parent_element_details.find_element(By.XPATH, "./following-sibling::*").text=="Preferred Candidate"
    except:
        pass
    
    if preferred:
        print("Preferred found")
        parent_element_preffered=get_element_by_xpath(driver,'//*[@id="view_inner"]/div/div[2]/dl[2]')

    
    if parent_element_preffered:
        # Find child elements within the <dl> element
        child_elements_preffered = parent_element_preffered.find_elements(By.XPATH, ".//*")
        
        for child in child_elements_preffered:
            try:
                # Extract the <dt> and <dd> elements
                dt_element = child.find_element(By.TAG_NAME, "dt")
                dd_element = child.find_element(By.TAG_NAME, "dd")

                # Get the text content of <dt> and <dd> elements and add it to the dictionary
                info_dict_preffered[dt_element.text] = dd_element.text
            except:
                pass
    
    # Add the job data dictionary to the list
    job_data = {"Job ID": job_id,"Description":job_description, "Skills":skills,"Preferred":info_dict_preffered, "Data": info_dict_general}

    with open(f'data_store/{job_id}.json', "w", encoding="utf-8") as json_file:
        json.dump(job_data, json_file, ensure_ascii=False, indent=4)



if __name__=="__main__":   
    # Read the JSON file as a list of job IDs
    with open("all_job_ids.json", "r") as json_file:
        job_ids = json.load(json_file)

    
    # Find new Job IDs that haven't been loaded
    new_ids = [job_id for job_id in job_ids if job_id not in get_scraped_ids('data_store')]

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    [get_job_info(driver,id) for id in new_ids]

    # Quit the WebDriver after all new jobs have been processed
    driver.quit()
