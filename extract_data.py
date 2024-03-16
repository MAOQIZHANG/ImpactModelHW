import os
import tarfile

# Directory containing both trades and quotes folders
parent_directory = '/Users/chenjiaying/Desktop/hw2_data' #replace by ur name

types_of_data = ['trades', 'quotes']

for type in types_of_data:
    # Directory to extract the contents of the .tar.gz files
    extract_directory = os.path.join('data', type)

    # Iterate through all files in the directory
    for file_name in os.listdir(os.path.join(parent_directory, type)):
        # Check if the file ends with .tar.gz
        if file_name.endswith('.tar.gz'):
            # Extract the date from the file name
            date = file_name.split('.')[0]
            # Check if the file name matches the format YYYYMMDD.tar.gz
            if len(date) == 8 and date.isdigit():
                # Construct the full path to the file
                file_path = os.path.join(parent_directory, type, file_name)
                # Create a directory to extract the contents if it doesn't exist
                # Extract the contents of the .tar.gz file
                with tarfile.open(file_path, 'r:gz') as tar:
                    tar.extractall(path=extract_directory)
                    print(f"Extracted {file_name} to {extract_directory}")

# Name of the file containing a list of S&P500 stocks
filter_file_name = 'SP500.txt'

with open(filter_file_name, 'r') as file:
    # get the tickers of S&P 500 stocks
    sp500_tickers = [line.strip() for line in file.readlines()]

# Remove files that are not of interest, i.e. non sp500 stocks
for type in types_of_data:
    # Directory containing the uncompressed files
    extract_directory = os.path.join('data', type)

    for daily_directory in os.listdir(extract_directory):
        
        for stock_directory in os.listdir(os.path.join(extract_directory, daily_directory)):
            
            co_tick = stock_directory.rsplit('_', 1)[0]

            if co_tick not in sp500_tickers:
                os.remove(os.path.join(extract_directory, daily_directory, stock_directory))