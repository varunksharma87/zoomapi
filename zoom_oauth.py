import os
import requests
from requests.auth import HTTPBasicAuth



def get_access_token():
    # Set the client credentials
    client_id = 'XXXXXXXXXXXXXXXXX'
    client_secret = 'XXXXXXXXXXXXXXXXX'

    # Set the authorization server's token endpoint URL
    token_url = 'https://zoom.us/oauth/token?grant_type=account_credentials&account_id=XXXXXXXXXXXXXXXXX'

    # Send a POST request to the token endpoint to get the access token
    response = requests.post(token_url, auth=HTTPBasicAuth(client_id, client_secret))

    # Check if the request was successful
    if response.status_code == 200:
        access_token = response.json()['access_token']
        #print('Access Token:', access_token)
        print('New Access Token Generated.')
        return access_token
    else:
        print('Error:', response.json())
        return None

def check_access_token():

    # Set the token file path
    token_file_path = 'access_token.txt'

    # Check if the token file exists
    if os.path.exists(token_file_path):
        # Read the access token from the file
        with open(token_file_path, 'r') as token_file:
            access_token = token_file.read().strip()
    else:
        # Generate a new access token
        access_token = get_access_token()
        # Save the access token to the file
        with open(token_file_path, 'w') as token_file:
            token_file.write(access_token)

    # Set the protected resource endpoint URL
    protected_url = 'https://api.zoom.us/v2/groups'

    # Set the authorization header with the access token
    headers = {'Authorization': f'Bearer {access_token}'}

    # Send a GET request to the protected resource endpoint
    response = requests.get(protected_url, headers=headers)

    # Check if the request was successful or requires token refresh
    if response.status_code == 200:
        data = response.json()
        #print('Response:', data)
        print('Access Token is Active. We are good to Go.')
    elif response.status_code == 401:  # Unauthorized (token expired)
        print('Token expired. Generating a new token...')
        access_token = get_access_token()
        if access_token:
            # Save the new access token to the file
            with open(token_file_path, 'w') as token_file:
                token_file.write(access_token)
            print('Testing New Access Token...')
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(protected_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                print('Access Token Worked. We are good to Go.')
            else:
                print('Error:', response.json())
    else:
        print('Error:', response.json())


check_access_token()
