import os
import re
import sys
import tarfile

current_script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_script_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Directory containing both trades and quotes folders
parent_directory = '/Users/chenjiaying/Desktop/hw2_data' #replace by ur name

types_of_data = ['trades', 'quotes']

def extract_data(parent_directory, types_of_data):
    for type in types_of_data:
        # Directory to extract the contents of the .tar.gz files
        extract_directory = os.path.join('data', type)

        # Ensure the base extract directory exists
        if not os.path.exists(extract_directory):
            os.makedirs(extract_directory)

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

                    # Extract the contents of the .tar.gz file
                    extract_tmp = os.path.join(extract_directory, file_name[:8])
                    if not os.path.exists(extract_tmp):
                        # If it doesn't exist, extract the contents of the .tar.gz file
                        with tarfile.open(file_path, 'r:gz') as tar:
                            tar.extractall(path=extract_directory)
                            print(f"Extracted {file_name} to {extract_directory}")
                    else:
                        print(f"Directory for {file_name} already exists, skipping extraction.")

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
    print("finish extracting data")

def check_data():
    # Regular expression to match folders with format YYYYMMDD
    date_format_regex = re.compile(r'^\d{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])$')

    # Directories
    trades_dir = os.path.join(parent_dir, "data/trades")
    quotes_dir = os.path.join(parent_dir, "data/quotes")

    # Check Trades Directory
    trades_count = 0
    for item in os.listdir(trades_dir):
        if os.path.isdir(os.path.join(trades_dir, item)) and date_format_regex.match(item):
            trades_count += 1

    # Check Quotes Directory
    quotes_count = 0
    for item in os.listdir(quotes_dir):
        if os.path.isdir(os.path.join(quotes_dir, item)) and date_format_regex.match(item):
            quotes_count += 1

    # Print check results
    print(f"Trades directories in correct format: {trades_count}")
    print(f"Quotes directories in correct format: {quotes_count}")

check_data()



