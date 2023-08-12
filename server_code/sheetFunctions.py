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
from .authenticationFunctions import refresh_access_token


# Common Smartsheet Client Initiation Code
def getSmartsheetClient(user):
    # print(user)
    # print(user['token_expiration'])
    current_time = datetime.now()
    token_expiration = user['token_expiration'].replace(tzinfo=None) if user['token_expiration'] else None
    # print(f"Current Time: {current_time}, Type: {type(current_time)}")
    # print(f"Token Expiration: {token_expiration}, Type: {type(token_expiration)}")

    if not token_expiration or current_time >= token_expiration:
        refresh_access_token(user)
    # After refreshing, get the updated user details with the new access token
    user = app_tables.users.get(email=user['email'])
    
    access_token = user['access_token']
    access_token = app_tables.users.get(email=user['email'])['access_token']
    client = smartsheet.Smartsheet(access_token)
    # print(client.Sheets.list_sheets())
    # client = smartsheet.Smartsheet(anvil.secrets.get_secret('smartsheetsKey'))
    return client

# Helper Function Do get Column Data based on criteria values using lambda
@anvil.server.callable
def getColumnDataWithCriteria(user, source_sheet_id, source_column_id, criteria_column_id, criteria_value, operator_keyword):
    # print(user)
    # print("source_sheet_id " + source_sheet_id)
    # print("source_column_id " + source_column_id)
    # print("criteria_column_id " + criteria_column_id)
    # print("criteria_value " + criteria_value)
    # print("operator_keyword " + operator_keyword)
    
    client = getSmartsheetClient(user)
    sheet = client.Sheets.get_sheet(source_sheet_id)
    criteria_column_obj = client.Sheets.get_column(source_sheet_id, criteria_column_id)
    source_column_obj = client.Sheets.get_column(source_sheet_id, source_column_id)
    columnValues = set()

    # Define a dictionary of lambda functions for each operator type
    operators = {
        "==": lambda x: x == criteria_value,
        "!=": lambda x: x != criteria_value,
        "contains": lambda x: criteria_value in x if x else False,
        "is_blank": lambda x: not x,
        "is_not_blank": lambda x: bool(x),
        "is_one_of": lambda x: x in criteria_value if isinstance(criteria_value, list) else False,
        "is_not_one_of": lambda x: x not in criteria_value if isinstance(criteria_value, list) else False,
        "between": lambda x: criteria_value[0] <= x <= criteria_value[1] if isinstance(criteria_value, list) and len(criteria_value) == 2 and x is not None else False
    }
    for row in sheet.rows:
        criteria_column_cell = row.get_column(criteria_column_obj.id)
        
        if criteria_column_cell:  # Check if the cell exists before accessing its value
            criteria_column_value = criteria_column_cell.value
        else:
            criteria_column_value = None
    
        # print(f"Checking if {criteria_column_value} == {criteria_value}")
    
        # Check if the value in the criteria column matches the specified criteria using the lambda functions
        if operators.get(operator_keyword, lambda x: False)(criteria_column_value):
            # print(f"Match found for {criteria_column_value}")
            
            source_column_cell = row.get_column(source_column_obj.id)
            if source_column_cell:  # Check if the cell exists before accessing its value
                columnCellValues = source_column_cell.value
    
                # If the column type is a contact type, convert values to contact dictionaries
                if source_column_obj.type in ["CONTACT_LIST", "MULTI_CONTACT_LIST"] and columnCellValues:
                    contacts = [{"email": email, "name": email} for email in [columnCellValues] if email]
                    for contact in contacts:
                        columnValues.add(str(contact))
                else:
                    columnValues.add(columnCellValues)
    
    # Convert the set of strings back to dictionaries if the column type is a contact type
    if source_column_obj.type in ["CONTACT_LIST", "MULTI_CONTACT_LIST"]:
        columnValues = [eval(contact_str) for contact_str in columnValues]
    
    return list(columnValues)


# Helper Function to get Total sheets in account
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


# Helper Function to get all sheet names and ID's into a dictionary
@anvil.server.callable
def getSheetData(user):
    client = getSmartsheetClient(user)
    response = client.Sheets.list_sheets(include_all=True)
    responseData = response.data

    # Transform response data into a list of dictionaries
    sheets = [{'sheet_id': str(sheet.id), 'sheet_name': sheet.name} for sheet in responseData]
  
    return sheets

# Helper Function to get column names and ID's
@anvil.server.callable
def getColumnNames(sheetId, user):
  client = getSmartsheetClient(user)
  response = client.Sheets.get_columns(sheet_id=sheetId,include_all=True, level=2)
  responseData = response.data
  # print(response)
  columns = [{'id': str(column.id), 'title': column.title} for column in responseData]
  return columns

# Helper Function to get column data without any criteria
@anvil.server.callable
def getColumnData(user, sheetId, ColumnId):
    client = getSmartsheetClient(user)
    sheet = client.Sheets.get_sheet(sheetId)
    column = client.Sheets.get_column(sheetId, ColumnId)
    columnValues = set()

    for row in sheet.rows:
        column_values = row.get_column(column.id).value
        if column_values:
            columnCellValues = column_values
            columnValues.add(columnCellValues)

        # If the column type is a contact type, convert values to contact dictionaries
    if column.type in ["CONTACT_LIST", "MULTI_CONTACT_LIST"]:
        # contacts = [create_contact(email) for email in columnValues if email]
        contacts = [{"email": email, "name": email} for email in columnValues if email]
        # print(type(contacts))
        # print(contacts)
        unique_column_values = contacts
    else:
        unique_column_values = list(columnValues)

    return unique_column_values

# Helper Function to get column data for DropDown Objects
@anvil.server.callable
def get_colum_data_for_ui(user, sheetId, ColumnId):
    client = getSmartsheetClient(user)
    sheet = client.Sheets.get_sheet(sheetId)
    column = client.Sheets.get_column(sheetId, ColumnId)
    columnValues = set()
    # print(column)

    for row in sheet.rows:
        column_values = row.get_column(column.id).value
        if column_values:
            columnCellValues = column_values
            columnValues.add(columnCellValues)

        # If the column type is a contact type, convert values to contact dictionaries
    if column.type in ["CONTACT_LIST", "MULTI_CONTACT_LIST"]:
        # contacts = [create_contact(email) for email in columnValues if email]
        contacts = [email for email in columnValues if email]
        # emails = [email for email in columnValues if email]
        # print(type(contacts))
        # print(contacts)
        unique_column_values = contacts
    else:
        unique_column_values = list(columnValues)

    return unique_column_values


def get_column_data_without_criteria(smartsheet_api_obj, sheet_id, Column_id):
    # client = getSmartsheetClient(user)
    get_sheet_obj = smartsheet_api_obj.Sheets.get_sheet(sheet_id)
    get_column_obj = smartsheet_api_obj.Sheets.get_column(sheet_id, Column_id)
    columnValues = set()

    for row in get_sheet_obj.rows:
        column_values = row.get_column(get_column_obj.id).value
        if column_values:
            columnCellValues = column_values
            columnValues.add(columnCellValues)

        # If the column type is a contact type, convert values to contact dictionaries
    if get_column_obj.type in ["CONTACT_LIST", "MULTI_CONTACT_LIST"]:
        # contacts = [create_contact(email) for email in columnValues if email]
        contacts = [{"email": email, "name": email} for email in columnValues if email]
        # print(type(contacts))
        # print(contacts)
        unique_column_values = contacts
    else:
        unique_column_values = list(columnValues)

    return unique_column_values