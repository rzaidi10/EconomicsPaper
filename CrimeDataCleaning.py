import pandas as pd
from uszipcode import SearchEngine
from collections import Counter


def get_zipcode_from_lat_long(lat, long):
    search = SearchEngine()
    result = search.by_coordinates(lat, long, radius=10, returns=1)
    return result[0].zipcode if result else None


def process_csv(input_file, output_file):
    df = pd.read_csv(input_file)

    # Remove rows with missing latitude or longitude
    df = df.dropna(subset=['LATITUDE', 'LONGITUDE'])
    print(
        f"Number of instances with incomplete latitude or longitude: {len(df[df[['LATITUDE', 'LONGITUDE']].isna().any(axis=1)])}")

    # Find zipcode for each instance
    df['ZIPCODE'] = df.apply(lambda row: get_zipcode_from_lat_long(row['LATITUDE'], row['LONGITUDE']), axis=1)

    # Count the frequency of each zipcode
    counter = Counter(df['ZIPCODE'])

    # Create a new dataframe from the counter
    new_df = pd.DataFrame.from_dict(counter, orient='index').reset_index()
    new_df.columns = ['ZIPCODE', 'Frequency']

    # Save the new dataframe as a CSV
    new_df.to_csv(output_file, index=False)


# Define the input and output file paths
input_file_path = "/Users/razazaidi/Downloads/Crimes_-_Map.csv"
output_file_path = "/Users/razazaidi/Desktop/zips.csv"

# Call the function
process_csv(input_file_path, output_file_path)
