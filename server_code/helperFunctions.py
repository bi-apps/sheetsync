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
from datetime import datetime, timedelta
from .authenticationFunctions import get_smartsheet_client_object


# Helper Function to Get the result code if Sucessfull or return the error message if error
def background_get_result_code_or_message(updated_destination_column):
    if isinstance(updated_destination_column, smartsheet.models.Error):
        return updated_destination_column.result.message
    else:
        return updated_destination_column.result_code

# Helper Function to Get the result code if Sucessfull or return the error message if error
def get_result_code_or_message(updated_destination_column):
    if isinstance(updated_destination_column, smartsheet.models.Error):
        return updated_destination_column.result.message
    else:
        return updated_destination_column.result_code

# Helper function to convert response values to contact dictionaries
def create_contact(email):
    return {"email": email, "name": email}

# Helper function to convert response values to contact lists for DropDowns
def create_contact_list_for_dropdowns(email):
    return [email]

# Helper Function To Check that Automation Name is unique
@anvil.server.callable
def is_mapping_name_unique(user, mapping_name, mapping_table):
    # Check if there is any existing row with the same mapping name for the user
    existing_mappings = mapping_table.search(user=user, map_name=mapping_name)
    if len(existing_mappings) == 0:
      return True
    else:
      return False

# Check if system should execute the automation
def should_execute(last_executed, threshold_minutes):
    """
    Determine if a job should be executed based on the last execution time and a threshold.
    
    Parameters:
    - last_executed: The datetime when the job was last executed.
    - threshold_minutes: The number of minutes that should elapse before the job is executed again.
    
    Returns:
    - True if the job should be executed, False otherwise.
    """
    if last_executed is None:
        return True
    
    # Ensure both datetimes are offset-naive
    now = datetime.now()
    if last_executed.tzinfo is not None:
        last_executed = last_executed.replace(tzinfo=None)
    if now.tzinfo is not None:
        now = now.replace(tzinfo=None)

    time_since_last_execution = now - last_executed
    
    print("Time Since Last Executed")
    print(time_since_last_execution)
    
    if time_since_last_execution >= timedelta(minutes=threshold_minutes):
        return True

    return False


@anvil.server.callable
def getLimitedSheetData(user, limit=100):
   client = get_smartsheet_client_object(user)
   response = client.Sheets.list_sheets(page_size=limit)
   # print(response)
   responseData = response.data
   
   sheets = [{'sheet_id': str(sheet.id), 'sheet_name': sheet.name} for sheet in responseData]
   return sheets

@anvil.server.callable
def searchSheets(user, search_string):
   client = get_smartsheet_client_object(user)
   response = client.Sheets.list_sheets(include_all=True)
   responseData = response.data
   
   # Filter sheets server-side and convert to dictionary
   filtered_sheets = [{'sheet_id': str(sheet.id), 'sheet_name': sheet.name} 
                      for sheet in responseData if search_string in sheet.name.lower()]
   
   return filtered_sheets


@anvil.server.callable
def check_logged_in():
    user = anvil.users.get_user()
    if user:
        return True
    return False
