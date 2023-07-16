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

        # Save the tokens
        anvil.tables.app_tables.auth_data.delete_all_rows()
        anvil.tables.app_tables.auth_data.add_row(access_token=access_token, refresh_token=refresh_token)

    except Exception as e:
        # Log the error and then redirect
        print(f"Error during OAuth callback: {e}")
        authenticated = False  
        return anvil.server.HttpResponse(status=302, headers={'Location': f'https://uz77gc6xsofjwhzw.anvil.app/752S2LMMMJ6U2I2NJVGEN4VM?authenticated={authenticated}'})
    
    finally:
        # Always redirect, even if there was an error
        authenticated = True  
        return anvil.server.HttpResponse(status=302, headers={'Location': f'https://uz77gc6xsofjwhzw.anvil.app/752S2LMMMJ6U2I2NJVGEN4VM?authenticated={authenticated}'})

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
@anvil.server.callable
def smartApi():
    # Initiate the Smartsheet client
  smart = smartsheet.Smartsheet(anvil.secrets.get_secret('smartsheetsKey'))
  
  # Set your desired page size
  page_size = 100
  # Get the total count of sheets
  total_count = smart.Sheets.list_sheets(page_size=1).total_count
  # Calculate the number of pages
  pages = math.ceil(total_count / page_size)
  
  all_sheet_names = []
  
  # Loop through all pages
  for page_number in range(1, pages + 1):
    # Fetch the page of results
    response = smart.Sheets.list_sheets(page_size=page_size, page_number=page_number)
    # Extract the data from the response
    sheets = response.data

    # Extract the names and add them to the list
    for sheet in sheets:
      all_sheet_names.append(sheet.name)
    
  return all_sheet_names
  
  # smart = smartsheet.Smartsheet(anvil.secrets.get_secret('smartsheetsKey'))             
  # response = smart.Sheets.list_sheets()
  # sheets = response.data   
  # print(sheets[0])
  # for sheet in sheets:
  #   try:
  #     sheet_id = str(sheet.id)
  #     sheet_name = sheet.name
  #     print(f"Adding row: ID={sheet_id}, Name={sheet_name}")
  #     app_tables.sheets.add_row(sheet_id=sheet_id,sheet_name=sheet_name)
  #   except Exception as e:
  #     print(f"Error when adding row: {e}")

@anvil.server.callable
def getSheets():
    # Initiate the Smartsheet client
  smart = smartsheet.Smartsheet(anvil.secrets.get_secret('smartsheetsKey'))
  
  # Set your desired page size
  page_size = 100
  # Get the total count of sheets
  total_count = smart.Sheets.list_sheets(page_size=1).total_count
  # Calculate the number of pages
  pages = math.ceil(total_count / page_size)
  
  all_sheet_names = []
  
  # Loop through all pages
  for page_number in range(1, pages + 1):
    # Fetch the page of results
    response = smart.Sheets.list_sheets(page_size=page_size, page_number=page_number)
    # Extract the data from the response
    sheets = response.data

    # Extract the names and add them to the list
    for sheet in sheets:
      all_sheet_names.append(sheet.name)
    
  return len(all_sheet_names)