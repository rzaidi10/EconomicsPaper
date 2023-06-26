import requests
import csv
from bs4 import BeautifulSoup
import os

# Define the URL to scrape
url = "https://fred.stlouisfed.org/release/tables?rid=249&eid=259515&od=#"

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find the table containing the desired data
table = soup.find("table")

# Define lists to store the data
states = []
median_incomes = []

# Extract the data from the table rows
for row in table.find_all("tr"):
    state_element = row.find("td", class_="fred-rls-elm-nm-cntnr fred-rls-elm-nm-td")
    income_element = row.find("td", class_="fred-rls-elm-vl-td")
    if state_element and income_element:
        states.append(state_element.text.strip())
        median_incomes.append(income_element.text.strip())


# Define the path to save the CSV file
desktop_path = os.path.expanduser("~/Desktop")
csv_file_path = os.path.join(desktop_path, "2021_median_income.csv")

# Write the data to the CSV file
with open(csv_file_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["State", "2021"])  # Write the header
    writer.writerows(zip(states, median_incomes))  # Write the data rows

print("Data has been scraped and saved as a CSV file on the desktop.")
