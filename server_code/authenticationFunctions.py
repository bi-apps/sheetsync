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

# Common Smartsheet Client Initiation Code
def get_smartsheet_client_object(user):
  access_token = app_tables.users.get(email=user['email'])['access_token']
  client = smartsheet.Smartsheet(access_token)
  # print(client.Sheets.list_sheets())
  # client = smartsheet.Smartsheet(anvil.secrets.get_secret('smartsheetsKey'))
  return client


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

        user.update(access_token=access_token, refresh_token=refresh_token, authenticated_to_smartsheets=True)

    except Exception as e:
        # Log the error and then redirect
        print(f"Error during OAuth callback: {e}")
        authenticated = False  
        return anvil.server.HttpResponse(status=302, headers={'Location': f'https://uz77gc6xsofjwhzw.anvil.app/752S2LMMMJ6U2I2NJVGEN4VM?authenticated={authenticated}'})
    
    finally:
        # Always redirect, even if there was an error
        return anvil.server.HttpResponse(status=302, headers={'Location': 'https://uz77gc6xsofjwhzw.anvil.app/752S2LMMMJ6U2I2NJVGEN4VM'})
      