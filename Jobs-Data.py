import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_job_info(job_id):
    job_url = f'https://www.bayt.com/en/international/jobs/?jobId={job_id}'
    driver.get(job_url)

    while True:
        try:
            parent_element = driver.find_element(By.XPATH, '//*[@id="view_inner"]/div/div[2]/dl[1]')
            break
        except:
            pass

    # Find child elements within the <dl> element
    child_elements = parent_element.find_elements(By.XPATH, ".//*")

    # Create a dictionary to store the extracted information
    info_dict = {}

    # Loop through child elements and extract the data
    for child in child_elements:
        try:
            # Extract the <dt> and <dd> elements
            dt_element = child.find_element(By.TAG_NAME, "dt")
            dd_element = child.find_element(By.TAG_NAME, "dd")

            # Get the text content of <dt> and <dd> elements and add it to the dictionary
            info_dict[dt_element.text] = dd_element.text
        except:
            pass
    # Add the job data dictionary to the list
    job_data_list.append({"Job ID": job_id, "Data": info_dict})

    
# Read the JSON file as a list of job IDs
with open("all_job_ids.json", "r") as json_file:
    job_ids = json.load(json_file)

# Initialize an empty list to store job data
job_data_list = []

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

[get_job_info(id) for id in job_ids]

# Save the job data list to a JSON file
with open("job_data.json", "w", encoding="utf-8") as json_file:
    json.dump(job_data_list, json_file, ensure_ascii=False, indent=4)

# Quit the WebDriver
driver.quit()
