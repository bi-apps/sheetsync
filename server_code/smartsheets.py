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
import base64
from cryptography.fernet import Fernet
from datetime import datetime

# Start Server Code
from anvil import Container

class RowPanel(Container):
    def __init__(self, **properties):
        super().__init__(**properties)
        self.role = "row"
        self.add_class("flow-panel")
        self.add_class("flow-spacing-small")

# ---------------- HELPER FUNCTIONS ------------------------- #
# Helper function to convert response values to contact dictionaries
def create_contact(email):
    return {"email": email, "name": email}

# Helper Function to Get the result code if Sucessfull or return the error message if error
def get_result_code_or_message(updated_destination_column):
    if isinstance(updated_destination_column, smartsheet.models.Error):
        return updated_destination_column.result.message
    else:
        return updated_destination_column.result_code

# ---------------- END HELPER FUNCTIONS --------------------- #

# Common Smartsheet Client Initiation Code
def getSmartsheetClient(user):
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
# End Encryption and Encryption Keys

# End Server Code

# indexPage Line 29
@anvil.server.callable
def check_auth_status(user):
      if user['authenticated_to_smartsheets'] is not True:
        authenticated = False
        return authenticated
        
      authenticated = True
      return authenticated

# indexPage Line 51
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
      
@anvil.server.callable
def getSheetsCount(user):
    client = getSmartsheetClient(user)
    # Call smartsheets API and retrive all sheets
    response = client.Sheets.list_sheets(include_all=True)
    # Get total sheet count from response
    total_count = response.total_count 
  
    # Get User sheet count, and if the count is the same don't update it, else update it
    if user['totalSheetsInAccount'] is not total_count:
      print('updating Sheet Count')
      user.update(totalSheetsInAccount=total_count)
      return True
      
    return True

@anvil.server.callable
def getSheetData(user):
    client = getSmartsheetClient(user)
    response = client.Sheets.list_sheets(include_all=True)
    responseData = response.data

    # Transform response data into a list of dictionaries
    sheets = [{'sheet_id': str(sheet.id), 'sheet_name': sheet.name} for sheet in responseData]
  
    return sheets

@anvil.server.callable
def getColumnNames(sheetId, user):
  client = getSmartsheetClient(user)
  response = client.Sheets.get_columns(sheet_id=sheetId,include_all=True, level=2)
  responseData = response.data
  # print(response)
  columns = [{'id': str(column.id), 'title': column.title} for column in responseData]
  return columns

@anvil.server.callable
def getColumnData(user, sheetId, ColumnId):
    client = getSmartsheetClient(user)
    sheet = client.Sheets.get_sheet(sheetId)
    column = client.Sheets.get_column(sheetId, ColumnId)
    columnValues = set()

    for row in sheet.rows:
        columnCellValues = row.get_column(column.id).value
        columnValues.add(columnCellValues)

    # If the column type is a contact type, convert values to contact dictionaries
    if column.type in ["CONTACT_LIST", "MULTI_CONTACT_LIST"]:
        # contacts = [create_contact(email) for email in columnValues if email]
        contacts = [{"email": email, "name": email} for email in columnValues if email]
        print(type(contacts))
        print(contacts)
        unique_column_values = contacts
    else:
        unique_column_values = list(columnValues)

    return unique_column_values

  
@anvil.server.callable
def runMappingTest(user_obj, source_sheet_id, source_column_id, destination_sheet_id, destination_column_id, destination_column_type, validation_on_destination_column=False, criteria_type=None, criteria_based_on=None, criteria_based_on_colum=None, criteria_value=None):
  # Initial Smartsheet Client Connection
  client = getSmartsheetClient(user_obj)
  # Get New Column Values from Selected Source Sheet and Column
  getNewColumnValues = getColumnData( user_obj, source_sheet_id, source_column_id)
  # Get Existing Selected Destination Sheet Columns Object
  getCurrentDestinationColumnOptions = client.Sheets.get_column(sheet_id=destination_sheet_id, column_id=destination_column_id)
  # Build Column Object
  # If the Destination Selected Column Type is not Contact column types Continue as normal dropdowns
  if destination_column_type not in ["CONTACT_LIST", "MULTI_CONTACT_LIST"]:
      new_column_obj = {
          "options": getNewColumnValues,
          "type": destination_column_type,
          "validation": validation_on_destination_column
      }
  else:
      # If the Destination Column type is a Contact Column Type build the Contact Dropdown Column Object
      # ---------------- Conect Column Type Specific Code ------------------------ #
      new_column_obj = {
          "contact_options": getNewColumnValues,
          "type": destination_column_type,
          "validation": validation_on_destination_column
      }
  # Update the Destination Sheet with the New Destination Column Values
  updated_destination_column = client.Sheets.update_column(
    sheet_id=destination_sheet_id,
    column_id=destination_column_id,
    column_obj=new_column_obj
  )
  # Return the call result
  return get_result_code_or_message(updated_destination_column)


@anvil.server.callable
def is_mapping_name_unique(user, mapping_name, mapping_table):
    # Check if there is any existing row with the same mapping name for the user
    existing_mappings = mapping_table.search(user=user, map_name=mapping_name)
    if len(existing_mappings) == 0:
      return True
    else:
      return False


@anvil.server.callable
def saveMapping(*args, **kwargs):
    # Try Saving the data to the Database based on the Mapping Type
    if kwargs['map_type'] == 1:
         try:
           kwargs['database'].add_row(
             
             user=kwargs['user_obj'],

             map_enabled=kwargs['map_enabled'],
             map_name=kwargs['map_name'],
             
             src_sheet_name=kwargs['source_sheet_name'],
             src_sheet_id=kwargs['source_sheet_id'],
             src_sheet_col_name=kwargs['source_column_name'],
             src_sheet_col_id=kwargs['source_colum_id'],
             
             dest_sheet_name=kwargs['destination_sheet_name'],
             dest_sheet_id=kwargs['destination_sheet_id'],
             dest_col_name=kwargs['destination_column_name'],
             dest_col_id=kwargs['destination_colum_id'],
             dest_column_type=kwargs['destination_colum_type'],
             dest_column_validation=kwargs['destination_column_validation'],

             created_DateStamp=datetime.now()
           )
           return True
         except tables.TableError as saveError:
           return str(saveError)