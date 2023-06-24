import requests
from bs4 import BeautifulSoup
import csv
import os
import pandas as pd

# Target URLs
urls = ["https://www.usnews.com/best-colleges/rankings/national-universities",
        "https://www.usnews.com/best-colleges/rankings/national-liberal-arts-colleges"]

# Prepare for storing the scraped data
data = []

# Loop over each URL
for url in urls:
    # Send a GET request
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find the list of colleges
    colleges = soup.select('.rankings-list-item')
    # Loop over each college
    for college in colleges:
        # Extract and print the name of the college and its rank
        name = college.select_one('.rankings-list-item__name').text.strip()
        link = "https://www.usnews.com" + college.select_one('.rankings-list-item__link')['href']
        # Follow the link to the college page and extract further details
        college_response = requests.get(link)
        college_soup = BeautifulSoup(college_response.text, 'html.parser')
        # Extract tuition and fees, graduation rate, US news ranking, class size, acceptance rate, and state
        tuition_fees_elem = college_soup.select_one('[data-testid="tuition-fees"]')
        tuition_fees = tuition_fees_elem.text.strip() if tuition_fees_elem is not None else ""
        graduation_rate_elem = college_soup.select_one('[data-testid="graduation-rate"]')
        graduation_rate = graduation_rate_elem.text.strip() if graduation_rate_elem is not None else ""
        acceptance_rate_elem = college_soup.select_one('[data-testid="acceptance-rate"]')
        acceptance_rate = acceptance_rate_elem.text.strip() if acceptance_rate_elem is not None else ""
        class_size_elem = college_soup.select_one('[data-testid="class-size"]')
        class_size = class_size_elem.text.strip() if class_size_elem is not None else ""
        state_elem = college_soup.select_one('.location')
        state = state_elem.text.strip().split(",")[-1].strip() if state_elem is not None else ""
        # Add the data to our storage
        data.append([name, tuition_fees, graduation_rate, class_size, acceptance_rate, state])
# Save the data to a CSV file
df = pd.DataFrame(data, columns=['Name', 'Tuition and Fees', 'Graduation Rate', 'Class Size', 'Acceptance Rate', 'State'])
# Sort by state
df = df.sort_values('State')
# Write the DataFrame to CSV
output_path = os.path.join(os.path.expanduser("~razazaidi"), "Desktop", 'USNewsData.csv')
df.to_csv(output_path, index=False, encoding='utf-8')