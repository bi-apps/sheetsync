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
from .helperFunctions import get_result_code_or_message, create_contact , is_mapping_name_unique
from .authenticationFunctions import create_user_encryption_key
from .sheetFunctions import getColumnDataWithCriteria, getSmartsheetClient, getSheetsCount, getSheetData, getColumnNames, getColumnData
from .databaseFunctions import saveMapping


# Start Server Code
from anvil import Container

class RowPanel(Container):
    def __init__(self, **properties):
        super().__init__(**properties)
        self.role = "row"
        self.add_class("flow-panel")
        self.add_class("flow-spacing-small")


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


