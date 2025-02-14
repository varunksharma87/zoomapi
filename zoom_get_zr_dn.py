import os
import requests
import csv
from requests.auth import HTTPBasicAuth
from zoom_oauth import check_access_token

def get_display_name(room_id):
    access_token = check_access_token()
    # Make a GET request to the API endpoint with the room ID
    endpoint = f'https://api.zoom.us/v2/rooms/{room_id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(endpoint, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        print(data)
        basic_info = data.get('basic', {})
        display_name = basic_info.get('display_name')
        print(display_name)
        return display_name
    else:
        print(f'Error retrieving display name for room ID: {room_id}')
        return None

def update_csv_with_display_names(csv_file):
    updated_rows = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        for row in reader:
            room_id = row['Room ID']
            print(room_id)
            display_name = get_display_name(room_id)
            if display_name is not None:
                row['Display Name'] = display_name
            updated_rows.append(row)

    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

# Specify the path to the CSV file
# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create the file path in the same directory as the script
csv_file_path = os.path.join(script_dir, 'rooms.csv')

# Call the function to update the CSV file with display names
update_csv_with_display_names(csv_file_path)
