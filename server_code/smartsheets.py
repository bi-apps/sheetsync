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
  apiKey = anvil.secrets.get_secret('smartsheetsKey')
  smart = smartsheet.Smartsheet(apiKey)             # Create a Smartsheet client 
  
  response = smart.Sheets.list_sheets()       # Call the list_sheets() function and store the response object
  sheetId = response.data          # Get the ID of the first sheet in the response
  # sheet = smart.Sheets.get_sheet(sheetId)     # Load the sheet by using its ID
  
  # print(f"The sheet {sheet.name} has {sheet.total_row_count} rows")   # Print information about the sheet
  return str(sheetId)
