import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By

def get_job_info(driver, job_id):
    print("Job Id", job_id)
    
    # Getting the URL
    job_url = f'https://www.bayt.com/en/international/jobs/?jobId={job_id}'
    driver.get(job_url)
    
    job_description = ""  # Initialize the job description string
    skills = []  # Initialize the skills list
    
    while True:
        try:
            # Find the starting point for job description
            job_description_start = driver.find_element(By.XPATH, '//*[@id="view_inner"]/div/div[2]/h2[2]')
            break
        except Exception as e:
            print(f"Error: {e}")
            pass
        
    # Iterate through siblings
    current_element = job_description_start
    while current_element is not None:
        # Check if the current element is a <p> tag
        if current_element.tag_name == "p":
            # Add the text of the <p> tag to the job description
            job_description += current_element.text
            # Check if the <p> tag contains a <br>, add a newline character
            if "<br>" in current_element.get_attribute("innerHTML"):
                job_description += "\n"
        
        # Check if we've reached the "Skills" section
        if "Skills" in current_element.text:
            skills_start = current_element
            break
        
        # Move to the next sibling
        current_element = current_element.find_element(By.XPATH, "./following-sibling::*")
    
    # Iterate through siblings starting from the "Skills" section
    current_element = skills_start
    while current_element is not None:
        # Check if the current element is a <p> tag
        if current_element.tag_name == "p":
            # Check if the <p> tag contains a <br>, add nothing
            if "<br>" not in current_element.get_attribute("innerHTML"):
                # Add the text of the <p> tag to the skills list
                skills.append(current_element.text)
        elif current_element.tag_name == "ul":
            skill_items = current_element.find_elements(By.TAG_NAME, "li")
            for item in skill_items:
                if "<br>" not in item.get_attribute("innerHTML"):
                    skills.append(item.text)
            
        # Check if we've reached the "Job Details" section
        if "Job Details" in current_element.text:
            break
        
        # Move to the next sibling
        current_element = current_element.find_element(By.XPATH, "./following-sibling::*")
    
    # Accessing the parent element for details
    while True:
        try:
            parent_element_details = driver.find_element(By.XPATH, '//*[@id="view_inner"]/div/div[2]/dl[1]')
            break
        except Exception as e:
            print(f"Error: {e}")
            pass
    
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
    
    # Accessing the parent element for preferred
    while True:
        try:
            parent_element_preffered = driver.find_element(By.XPATH, '//*[@id="view_inner"]/div/div[2]/dl[2]')
            break
        except Exception as e:
            print(f"Error: {e}")
            pass
    
    # Find child elements within the <dl> element
    child_elements_preffered = parent_element_preffered.find_elements(By.XPATH, ".//*")
    
    # Create a dictionary to store the extracted information concerning preferred
    info_dict_preffered = {}
    
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

    print(job_data)
    
    

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
get_job_info(driver,69872937)
# Quit the WebDriver after all new jobs have been processed
driver.quit()
