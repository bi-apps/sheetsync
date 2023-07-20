from ._anvil_designer import oneToOneSetupTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class oneToOneSetup(oneToOneSetupTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Get User
        user = anvil.users.get_user()
        # Any code you write here will run before the form opens.
        sheet_data = anvil.server.call('getSheetData', user)
        # Create a dictionary to map sheet names to sheet IDs
        self.sheet_map = {sheet['sheet_name']: sheet['sheet_id'] for sheet in sheet_data}
        # Set the dropdown items to be the sheet names
        self.oneToOneSourceSheetDropDown.items = list(self.sheet_map.keys())

        # Set the event handler for the dropdown's change event
        self.oneToOneSourceSheetDropDown.set_event_handler('change', self.oneToOneSourceSheetDropDown_change)
    
    def oneToOneSourceSheetDropDown_change(self, **event_args):
        """This method is called when an item is selected"""
        selectedSheetName = self.oneToOneSourceSheetDropDown.selected_value
        
        if selectedSheetName is not None:
            selectedSheetId = self.sheet_map[selectedSheetName]
            print(f"Selected Sheet ID: {selectedSheetId}")
