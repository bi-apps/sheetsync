import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import smartsheet
import math
import uuid
import requests
import anvil.http
import base64
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
from time import sleep

@anvil.server.callable
def get_smartsheet_client_object(user, max_retries=3, retry_delay=5):
    """
    Initiates a Smartsheet client. If the token is expired or invalid, it tries to refresh the token.
    If refreshing or any other operation fails, it retries up to max_retries times.

    Args:
    - user: The user object containing token information.
    - max_retries: The maximum number of retries if an operation fails.
    - retry_delay: The delay (in seconds) between retries.

    Returns:
    - Smartsheet client object.
    """
    
    current_time = datetime.now()
    
    # Accessing the token_expiration as per the specified manner
    token_expiration = user['token_expiration'].replace(tzinfo=None) if user['token_expiration'] else None
    
    retry_count = 0

    while retry_count < max_retries:
        try:
            # Check if the token is expired and refresh if necessary
            if not token_expiration or current_time >= token_expiration:
                refresh_access_token(user)
                user = app_tables.users.get(email=user['email'])
            
            access_token = user['access_token']
            
            if not access_token:
                raise ValueError("Access token not found for the user.")
            
            client = smartsheet.Smartsheet(access_token)
            return client

        except Exception as e:
            print("Entered the exception Block")
            print(e)
            retry_count += 1
            print(f"Error encountered: {e}. Retrying {retry_count}/{max_retries}...")
            sleep(retry_delay)

    raise ValueError("Failed to initiate Smartsheet client after maximum retries.")



# Handel Encryption and Encryption Keys
def create_user_encryption_key(user):
    # Generate a new encryption key
    user_encryption_key = Fernet.generate_key()

    # Convert the encryption key to a base64-encoded string
    encoded_key = base64.urlsafe_b64encode(user_encryption_key).decode()

    # Add user encryption key to users table
    user.update(url_encoded_encryption=encoded_key, encryption_key=str(user_encryption_key))
    
    return encoded_key

# indexPage Line 29 Check users Autentication Status
@anvil.server.callable
def check_auth_status(user):
     if user['authenticated_to_smartsheets'] is not True:
        authenticated = False
        return authenticated
        
     authenticated = True
     return authenticated

# indexPage Line 51 Get Authentication URL from Smartsheets
@anvil.server.callable
def get_auth_url(user):
    encoded_state = create_user_encryption_key(user)
    client_id = anvil.secrets.get_secret('smartsheetAppClientId') # Save your client id in secrets
    state = f"{uuid.uuid4()}_{encoded_state}"
    user.update(encryption_state=state)
    scope = 'READ_SHEETS WRITE_SHEETS ADMIN_SHEETS'
    auth_url = f"https://app.smartsheet.com/b/authorize?response_type=code&client_id={client_id}&scope={scope}&state={state}"
    print(f'URL Link {auth_url}')
    return auth_url

# Catch Get Request back from smartsheets call back URL
@anvil.server.http_endpoint("/oauth_callback")
def oauth_callback(**kwargs):
    try:
        # Potentially error-throwing code here
        code = kwargs.get('code')
        if not code:
            raise Exception("No code in URL parameters")
          
        state = kwargs.get('state')
        if not state:
            raise Exception("No User State Returned, Bail!")
          
        # Get user based on Encoded Encryption String
        user = tables.app_tables.users.get(encryption_state=state)
        
        
      
        client_id = anvil.secrets.get_secret('smartsheetAppClientId')
        client_secret = anvil.secrets.get_secret('smartsheetAppClientSecret')
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
        }
        response = requests.post('https://api.smartsheet.com/2.0/token', data=data)
        response.raise_for_status()
        access_token = response.json()['access_token']
        refresh_token = response.json()['refresh_token']
        token_type = response.json()['token_type']
        expires_in_seconds = response.json()['expires_in']
        # Calculate the exact time when the token will expire
        token_expiration_timestamp = datetime.now() + timedelta(seconds=expires_in_seconds)
        
        user.update(access_token=access_token, refresh_token=refresh_token, authenticated_to_smartsheets=True, token_type=token_type, token_expiration=token_expiration_timestamp, automation_count=0)

    except Exception as e:
        # Log the error and then redirect
        print(f"Error during OAuth callback: {e}")
        authenticated = False  
        return anvil.server.HttpResponse(status=302, headers={'Location': f'https://uz77gc6xsofjwhzw.anvil.app/AMCH7DKKMUWKPUAB7RZCKY3I?authenticated={authenticated}'})
    
    finally:
        # Always redirect, even if there was an error
        return anvil.server.HttpResponse(status=302, headers={'Location': 'https://uz77gc6xsofjwhzw.anvil.app/AMCH7DKKMUWKPUAB7RZCKY3I'})


def refresh_access_token(user):
    client_id = anvil.secrets.get_secret('smartsheetAppClientId')
    client_secret = anvil.secrets.get_secret('smartsheetAppClientSecret')
    
    # Get refresh token from user data
    refresh_token = user['refresh_token']
    
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret,
    }
    
    response = requests.post('https://api.smartsheet.com/2.0/token', data=data)
    
    # Check for bad status codes and log the response for debugging
    if response.status_code != 200:
        print(f"Error refreshing token. Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        response.raise_for_status()
    
    access_token = response.json().get('access_token')
    new_refresh_token = response.json().get('refresh_token', refresh_token)  # Use the old refresh token if a new one isn't provided
    
    # Update user data with new tokens
    user.update(access_token=access_token, refresh_token=new_refresh_token)
    
    return access_token

