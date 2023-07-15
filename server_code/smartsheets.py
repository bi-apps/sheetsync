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
  smart = smartsheet.Smartsheet(anvil.secrets.get_secret('smartsheetsKey'))             
  response = smart.Sheets.list_sheets()
  sheets = response.data   
  print(sheets[0])
  for sheet in sheets:
    try:
      sheet_id = str(sheet.id)
      sheet_name = sheet.name
      print(f"Adding row: ID={sheet_id}, Name={sheet_name}")
      app_tables.sheets.add_row(sheet_id=sheet_id,sheet_name=sheet_name)
    except Exception as e:
      print(f"Error when adding row: {e}")