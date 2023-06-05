import os
import requests
import csv
from requests.auth import HTTPBasicAuth
from zoom_oauth_v2 import check_access_token

def get_zr_ids():
    access_token = check_access_token()
    # Set the protected resource endpoint URL
    protected_url = 'https://api.zoom.us/v2/rooms'
    # Set the authorization header with the access token
    headers = {'Authorization': f'Bearer {access_token}'
               }

    # Send a GET request to the protected resource endpoint
    response = requests.get(protected_url, headers=headers)

    # Get Zoom rooms list
    if response.status_code == 200:
        data = response.json()
        rooms = data['rooms']
        
        save_as_text(rooms)  # Save as text file
        save_as_csv(rooms)
        print('Response: Success', data)

    else:
        print('Error:', response.json())

def save_as_text(rooms):
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create the file path in the same directory as the script
    file_path = os.path.join(script_dir, 'rooms.txt')
    with open(file_path, 'w') as file:
        for room in rooms:
            room_id = room['room_id']
            name = room['name']
            location_id = room['location_id']
            status = room['status']
            display_name = ''
            file.write(f'Location ID: {location_id}, Room ID: {room_id}, Name: {name}, Display Name: {display_name}, Status: {status} \n' )

def save_as_csv(rooms):
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create the file path in the same directory as the script
    file_path = os.path.join(script_dir, 'rooms.csv')
    fieldnames = ['Location ID','Room ID', 'Name', 'Display Name', 'Status']

    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for room in rooms:
            room_id = room['room_id']
            name = room['name']
            location_id = room['location_id']
            status = room['status']
            display_name = ''
            writer.writerow({'Location ID': location_id, 'Room ID': room_id, 'Name': name,  'Display Name': display_name, 'Status': status })

get_zr_ids()
