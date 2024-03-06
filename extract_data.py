import os
import tarfile

# Directory containing the .tar.gz files
directory = 'C:/Users/Alex/Downloads/trades-20240306T040221Z-001/trades' #replace by ur name

# Directory to extract the contents of the .tar.gz files
extract_directory = 'data/trades'

# Iterate through all files in the directory
for file_name in os.listdir(directory):
    # Check if the file ends with .tar.gz
    if file_name.endswith('.tar.gz'):
        # Extract the date from the file name
        date = file_name.split('.')[0]
        # Check if the file name matches the format YYYYMMDD.tar.gz
        if len(date) == 8 and date.isdigit():
            # Construct the full path to the file
            file_path = os.path.join(directory, file_name)
            # Create a directory to extract the contents if it doesn't exist
            # Extract the contents of the .tar.gz file
            with tarfile.open(file_path, 'r:gz') as tar:
                tar.extractall(path=extract_directory)
                print(f"Extracted {file_name} to {extract_directory}")
