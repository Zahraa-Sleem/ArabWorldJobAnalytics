import requests
from bs4 import BeautifulSoup
import json

def get_job_ids(page_id):
    print("Fetching page",page_id)
    url = f'https://www.bayt.com/en/international/jobs/?page={page_id}'
    headers = {
        'User-Agent': 'Your-User-Agent-String-Here'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.content
    else:
        print("Failed to retrieve the webpage")
        return []

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')

    # Select all <li> elements with class name containing "has-name-d"
    selected_li_elements = soup.select('li[class*="has-pointer-d"]')

    # Extract the value of the data-job-id attribute from each selected <li> element
    data_job_ids = [li.get('data-job-id') for li in selected_li_elements]

    # # Specify the path where you want to save the JSON data
    # output_file_path = f'job_ids_page_{page_id}.json'

    # # Save the extracted job IDs to a JSON file
    # with open(output_file_path, 'w') as json_file:
    #     json.dump(data_job_ids, json_file)

    return data_job_ids

# Initialize an empty list to store all job IDs
all_job_ids = []

# Iterate through pages 1 to 501
for page_id in range(59, 90):
    job_ids = get_job_ids(page_id)
    all_job_ids.extend(job_ids)

# Save all job IDs in a single JSON file
output_file_path = 'all_job_ids.json'
with open(output_file_path, 'w') as json_file:
    json.dump(all_job_ids, json_file)

# Now, all job IDs are saved in a single JSON file named 'all_job_ids.json'


