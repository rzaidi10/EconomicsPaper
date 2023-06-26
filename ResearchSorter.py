
import pandas as pd
import os
from collections import defaultdict
import requests
import json

# Your Mapbox API access token
MAPBOX_TOKEN = 'pk.eyJ1IjoicnphaWRpIiwiYSI6ImNsamNkaWM1MzB1bmUzZHFyamh6ajUwN28ifQ.MfsDDOxgRYif0hAr3I94dw'


def get_state(university):
    try:
        # Prepare API request
        url = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{university}.json?access_token={MAPBOX_TOKEN}'
        response = requests.get(url)
        data = json.loads(response.text)

        # Extract state from API response
        if data['features']:
            for feature in data['features']:
                for context in feature['context']:
                    if context['id'].startswith('region'):
                        return context['text']
    except Exception as e:
        print(f'Error occurred while finding state for university {university}: {e}')
    return None


# Load the xlsx file
filepath = os.path.expanduser("~/Desktop/EconomicsPaper/HERDrankings.xlsx")
df = pd.read_excel(filepath, header=None, skiprows=5, usecols=[0, 1], names=["Institution", "R&D expenditures"])

# Map universities to states and group R&D expenditures
state_expenditures = defaultdict(int)
for index, row in df.iterrows():
    state = get_state(row['Institution'])
    if state:
        state_expenditures[state] += row['R&D expenditures']

# Create a new DataFrame
new_df = pd.DataFrame(list(state_expenditures.items()), columns=['State', '2021'])

# Save the new DataFrame to a csv file
new_filepath = os.path.expanduser("~/Desktop/EconomicsPaper/State_Research.csv")
new_df.to_csv(new_filepath, index=False)
