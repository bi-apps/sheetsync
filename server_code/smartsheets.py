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
import anvil.secrets
import math
import uuid
import requests
import anvil.http



# smartsheets clieent ID's

# client id = "bhpzjjue0q7imkv65ri"
# appSecret = "f8h8fsqzb1dh1dbiyne"

def getSmartsheetClient(userId):
  access_token = app_tables.auth_data.get(user=userId)['access_token']
  # client = smartsheet.Smartsheet(access_token)
  client = smartsheet.Smartsheet(anvil.secrets.get_secret('smartsheetsKey'))
  return client

@anvil.server.callable
def get_auth_url():
    client_id = anvil.secrets.get_secret('smartsheetAppClientId') # Save your client id in secrets
    state = uuid.uuid4()
    scope = 'READ_SHEETS WRITE_SHEETS'
    auth_url = f"https://app.smartsheet.com/b/authorize?response_type=code&client_id={client_id}&scope={scope}&state={state}"
    
    return auth_url
  
@anvil.server.http_endpoint("/oauth_callback")
def oauth_callback(**kwargs):
    try:
        # Potentially error-throwing code here
        code = kwargs.get('code')
        if not code:
            raise Exception("No code in URL parameters")

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

        user_row = anvil.users.get_user()
        print(user_row)
        user = 'userId'
        
        # Save the tokens
        # anvil.tables.app_tables.auth_data.delete_all_rows()
        user_row.update(access_token=access_token, refresh_token=refresh_token, authenticated_to_smartsheets=True)
        # anvil.tables.app_tables.auth_data.add_row(access_token=access_token, refresh_token=refresh_token, authenticated=True, user="userId")
      
        getSheetsCount(user_row)
        getSheetData(user_row)

    except Exception as e:
        # Log the error and then redirect
        print(f"Error during OAuth callback: {e}")
        authenticated = False  
        return anvil.server.HttpResponse(status=302, headers={'Location': f'https://uz77gc6xsofjwhzw.anvil.app/752S2LMMMJ6U2I2NJVGEN4VM?authenticated={authenticated}'})
    
    finally:
        # Always redirect, even if there was an error
        return anvil.server.HttpResponse(status=302, headers={'Location': 'https://uz77gc6xsofjwhzw.anvil.app/752S2LMMMJ6U2I2NJVGEN4VM'})
      
@anvil.server.callable
def check_auth_status(user):
      # user_auth_data = tables.app_tables.auth_data.get(user=user)
      if user_auth_data is not None:
        authenticated = True
        return authenticated
        
      authenticated = False
      return authenticated

@anvil.server.callable
def getSheetsCount(userId):
    client = getSmartsheetClient(userId)
    # Call smartsheets API and retrive all sheets
    response = client.Sheets.list_sheets(include_all=True)
    # Get total sheet count from response
    total_count = response.total_count 
  
    # Get User sheet count, and if the count is the same don't update it, else update it
    getUserAuthData = tables.app_tables.auth_data.get(user=userId)
    if getUserAuthData['totalSheetsInAccount'] is not total_count:
      print('updated')
      getUserAuthData.update(totalSheetsInAccount=total_count)

    # Get all Sheet Names and Data Require
  
    # Return total count to calling client side code
    return

def getSheetData(userId):
    client = getSmartsheetClient(userId)
    response = client.Sheets.list_sheets(include_all=True)
    responseData = response.data

    for sheet in responseData:
        existing_sheet = tables.app_tables.sheets.get(sheet_id=str(sheet.id))

        if existing_sheet is not None:
            if existing_sheet['sheet_name'] != sheet.name:
                # Update the sheet name if it is different
                existing_sheet['sheet_name'] = sheet.name
                existing_sheet.save()
        else:
            # Add a new row if the sheet does not exist in the table
            tables.app_tables.sheets.add_row(
                sheet_id=str(sheet.id),
                sheet_name=sheet.name,
                user=userId
            )

  

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
