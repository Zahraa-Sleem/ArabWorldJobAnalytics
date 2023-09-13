import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_job_info(job_id, driver):
    print("Job Id", job_id)
    # Getting the url
    job_url = f'https://www.bayt.com/en/international/jobs/?jobId={job_id}'
    driver.get(job_url)

    # Accessing the parent element
    while True:
        try:
            parent_element = driver.find_element(By.XPATH, '//*[@id="view_inner"]/div/div[2]/dl[1]')
            break
        except Exception as e:
            print(f"Error: {e}")
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
    job_data = {"Job ID": job_id, "Data": info_dict}

    # Open the JSON file in append mode and write the job data
    with open("job_data.json", "a", encoding="utf-8") as json_file:
        json.dump(job_data, json_file, ensure_ascii=False,indent=4)
        json_file.write(",")

# Read the JSON file as a list of job IDs
with open("all_job_ids.json", "r") as json_file:
    job_ids = json.load(json_file)

# Initialize jobsloaded as an empty list
jobsloaded = []

# Check if the "job_data.json" file exists and is not empty
try:
    with open('job_data.json', 'r') as input_file:
        for line in input_file:
            if line.strip():  # Check if the line is not empty
                job_data = json.loads(line)
                jobsloaded.append(job_data)
except (FileNotFoundError, json.decoder.JSONDecodeError):
    # Handle the case where the file doesn't exist or is empty
    pass

# Extract existing Job IDs from loaded data
existing_ids = [job['Job ID'] for job in jobsloaded]

# Find new Job IDs that haven't been loaded
new_ids = [job_id for job_id in job_ids if job_id not in existing_ids]

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Iterate over new job IDs and get job information
[get_job_info(id,driver) for id in new_ids]

# Quit the WebDriver after all new jobs have been processed
driver.quit()
