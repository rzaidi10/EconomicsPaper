import pandas as pd
from googlesearch import search
import os
import re
from collections import defaultdict

def get_state(university):
    try:
        # Google search
        query = university + ' state'
        for j in search(query, num=1, stop=1, pause=2):
            # Extract state from search result
            match = re.search(r'in ([\w ]+),', j)
            if match:
                return match.group(1)
    except Exception as e:
        print(e)
    return None

# Load the xlsx file
filepath = os.path.expanduser("~/Desktop/EconomicsPaper/HERDrankings.xlsx")
df = pd.read_excel(filepath, header=None, skiprows=5, usecols=[0,1], names=["Institution", "R&D expenditures"])

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
