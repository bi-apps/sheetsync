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


# smartsheets clieent ID's

# client id = "bhpzjjue0q7imkv65ri"
# appSecret = "f8h8fsqzb1dh1dbiyne"

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