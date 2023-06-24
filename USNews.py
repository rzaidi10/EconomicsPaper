import requests
from bs4 import BeautifulSoup
import csv
import os
import pandas as pd

# Target URLs
url = "https://www.usnews.com/best-colleges/rankings/national-universities"

# Send a GET request
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the list of colleges
colleges = soup.select('.rankings-list')

# Prepare for storing the scraped data
data = []

# Loop over each college
for college in colleges:
    # Extract and print the name of the college and its rank
    name = college.select_one('.rankings-list-item__name').text
    link = "https://www.usnews.com" + college.select_one('.rankings-list-item__link')['href']

    # Follow the link to the college page and extract further details
    college_response = requests.get(link)
    college_soup = BeautifulSoup(college_response.text, 'html.parser')

    # Extract tuition and fees, graduation rate, US news ranking, class size, acceptance rate, and state
    details = college_soup.select_one('.quick-stats')
    if details is not None:
        tuition_fees = details.select_one('[data-testid="tuition-fees"]').text
        graduation_rate = details.select_one('[data-testid="grad-rate"]').text
        acceptance_rate = details.select_one('[data-testid="acceptance-rate"]').text
        class_size = details.select_one('[data-testid="class-size"]').text
        state = details.select_one('[data-testid="location"]').text.split(",")[-1].strip()

        # Add the data to our storage
        data.append([name, tuition_fees, graduation_rate, class_size, acceptance_rate, state])

# Save the data to a CSV file
df = pd.DataFrame(data, columns=['Name', 'Tuition and Fees', 'Graduation Rate', 'Class Size', 'Acceptance Rate', 'State'])

# Sort by state
df = df.sort_values('State')

# Write the DataFrame to CSV
df.to_csv(os.path.join(os.path.expanduser("~razazaidi"), "Desktop", 'USNewsData.csv'), index=False)
