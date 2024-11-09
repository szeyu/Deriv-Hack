import csv
from datetime import datetime
import os

def save_data_to_fallback_csv():
    file_path = os.path.join('..', 'database', 'fallback.csv') 

    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    print(f"Saving to {file_path}...") 

    # Automatically get the current datetime
    datetime_obj = datetime.now()  # Current date and time
    # print(f"Current datetime is: {datetime_obj}")  # Debugging print

    # Prompt for other data
    fallbackID = input("Enter fallbackID: ") #auto generated using panda 
    custID = input("Enter custID: ")#auto generated using panda
    status1 = input("Enter status1: ") #return the data and save here
    status2 = input("Enter status2: ") 
    status3 = input("Enter status3: ")

    # Store the data as a dictionary for easier writing to CSV
    data = {
        'fallbackID': fallbackID, 
        'custID': custID, 
        'datetime': datetime_obj.strftime("%Y-%m-%d %H:%M:%S"),  # Format the datetime
        'status1': status1,
        'status2': status2,
        'status3': status3
    }
    print("Data to save to fallback.csv:", data) 

    # Check if fallback.csv already has a header or is empty
    try:
        with open(file_path, 'r', newline='') as file:
            has_header = csv.Sniffer().has_header(file.read(1024))
    except FileNotFoundError:
        has_header = False

    # Append data to fallback.csv
    with open(file_path, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if not has_header:
            writer.writeheader()
        writer.writerow(data)

    print("Data saved successfully to fallback.csv!")


save_data_to_fallback_csv()