import requests
from requests.auth import HTTPBasicAuth

# Step 1: Get an access token from the authorization server

# Set the authorization server's token endpoint URL
token_url = 'https://zoom.us/oauth/token?grant_type=account_credentials&account_id=Od1Y5-cqTaicWW5dwvcgKA'

# Set the client credentials
client_id = 'KNnATDQQE1fVZLnwUPQw'
client_secret = 'LymWlJzLKSahH4GQ0aNJ64aEkUxGZSPA'

# Set the scope (optional)
#scope = 'read write'

# Set the grant type
grant_type = 'client_credentials'

# Send a POST request to the token endpoint to get the access token
response = requests.post(token_url, auth=HTTPBasicAuth(client_id, client_secret))

# Check if the request was successful
if response.status_code == 200:
    access_token = response.json()['access_token']
    print('Access Token:', access_token)
else:
    print('Error:', response.json())

# Step 2: Use the access token to access protected resources

# Set the protected resource endpoint URL
protected_url = 'https://api.zoom.us/v2/rooms'

# Set the authorization header with the access token
headers = {'Authorization': f'Bearer {access_token}'}

# Send a GET request to the protected resource endpoint
response = requests.get(protected_url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    print('Response:', data)
else:
    print('Error:', response.json())


