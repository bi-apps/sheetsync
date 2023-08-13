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
from datetime import datetime

class oneToOneSetup(oneToOneSetupTemplate):
    def __init__(self, user=None, setup_data=None, **properties):
    # def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.setup_data = setup_data
        print(f"Setup Data : {self.setup_data}")
        # Initiate Screen Object States
        # Disabled Main Flow Panel until Name is Selected
        # self.oneToOneSourceSheetCard.visible = False
      
        # Enabled States Disabled
        self.oneToOneSourceColumnDropDown.enabled = False
        self.oneToOneDestinationColumnDropDown.enabled = False
      
        # Buttons Flow Panel Visbility Off
        self.oneToOneButtonFlowPanel.visible = False
      
        # Buttons Disabled
        # self.oneToOneAddMappingAndRunBtn.enabled = False
        # self.oneToOneResetMappingFormBtn.enabled = False
      
        # Visablility Disabled
        self.oneToOneDestinationSheetCard.visible = False
        self.oneToOneFilterImageObject.visible = False

        # End Initiation of Screen Object States
      
        # Get User
        # self.user = user
        if user is None:
            self.user = anvil.users.get_user()
        else:
            self.user = user
      
        # Any code you write here will run before the form opens.
        # Get Sheet Names and Id's
        sheet_data = anvil.server.call('getSheetData', self.user)
      
        # Create a dictionary to map sheet names to sheet IDs
        self.sheet_map = {sheet['sheet_name']: sheet['sheet_id'] for sheet in sheet_data}
      
        # Set the dropdown items to be the sheet names
        self.oneToOneSourceSheetDropDown.items = list(self.sheet_map.keys())
        self.oneToOneDestinationSheetDropDown.items = list(self.sheet_map.keys())

        # If Data is sent from setup index setup button use this as the source sheet
        if self.setup_data:
            self.oneToOneSourceSheetDropDown.selected_value = self.setup_data['sheet_name']
            self.oneToOneSourceSheetDropDown_change()

        self.column_types_data = app_tables.column_types.search()
        # Populate the dropdown with 'columnName' values
        self.oneToOneDestinationDropdownType.items = [row['column_type'] for row in self.column_types_data]

        # Set the event handler for the dropdown's change event
        # self.oneToOneSourceSheetDropDown.set_event_handler('change', self.oneToOneSourceSheetDropDown_change)
    
    def oneToOneSourceSheetDropDown_change(self, **event_args):
        """This method is called when an item is selected"""
        # Get Selected Sheet Name and ID
        self.selSrcSheetName = self.oneToOneSourceSheetDropDown.selected_value
        
        if self.selSrcSheetName is not None:
            self.selectedSourceSheetId = self.sheet_map[self.selSrcSheetName]

            # Start Get Columns ----------------------------------------------------------------
            # Set Dropdown Source Coulmn State and Values
            self.oneToOneSourceColumnDropDown.enabled = True
            # Get Column Names for Selected Sheet and Insert Values into Dropdown
            columns_data = anvil.server.call('getColumnNames',self.selectedSourceSheetId, self.user)
            self.column_map = {column['title']: column['id'] for column in columns_data}
            self.oneToOneSourceColumnDropDown.items = list(self.column_map.keys())
            # End Get Columns ----------------------------------------------------------------
          


            print(f"Selected Source Sheet ID: {self.selectedSourceSheetId}")

    def sourceSheetColumnDropDown_change(self, **event_args):
        """This method is called when an item is selected"""
        # Get Selected Column ID
        self.selSrcColumnName = self.oneToOneSourceColumnDropDown.selected_value
          
        # Check Selected Column State
        if self.selSrcColumnName is not None:
            self.selectedSourceColumnId = self.column_map[self.selSrcColumnName]
            self.oneToOneDestinationSheetCard.visible = True
            # Enable Filter Image
            self.oneToOneFilterImageObject.visible = True

        print(f"Selected Source Column ID: {self.selectedSourceColumnId}")

    def oneToOneDestinationSheetDropDown_change(self, **event_args):
        """This method is called when an item is selected"""
        self.selDestSheetName = self.oneToOneDestinationSheetDropDown.selected_value

        if self.selDestSheetName is not None:
          self.selectedDestinationSheetId = self.sheet_map[self.selDestSheetName]

          # Start Get Columns ----------------------------------------------------------------
          # Set Dropdown Source Coulmn State and Values
          self.oneToOneDestinationColumnDropDown.enabled = True
          # Get Column Names for Selected Sheet and Insert Values into Dropdown
          columns_data = anvil.server.call('getColumnNames',self.selectedDestinationSheetId, self.user)
          self.column_map = {column['title']: column['id'] for column in columns_data}
          self.oneToOneDestinationColumnDropDown.items = list(self.column_map.keys())
          # End Get Columns ----------------------------------------------------------------
          print(f"Selected Destination Sheet ID: {self.selectedDestinationSheetId}")

    def oneToOneDestinationColumnDropDown_change(self, **event_args):
        """This method is called when an item is selected"""
        self.selDestColumnName = self.oneToOneDestinationColumnDropDown.selected_value

        if self.selDestColumnName is not None:
          self.selectedDestinationColumnId = self.column_map[self.selDestColumnName]
          # self.oneToOneAddMappingAndRunBtn.enabled = True
          # self.oneToOneResetMappingFormBtn.enabled = True
          self.oneToOneButtonFlowPanel.visible = True
        print(f"Selected Destination Column ID: {self.selectedDestinationColumnId}")

    def oneToOneDestinationDropdownType_change(self, **event_args):
        self.selectedColumnTypeName = self.oneToOneDestinationDropdownType.selected_value
        selected_row = next((row for row in self.column_types_data if row['column_type'] == self.selectedColumnTypeName), None)
      
        if self.selectedColumnTypeName:
           self.columnTypeValue = selected_row['column_type_value']
           self.columnTypeValidation = selected_row['column_type_validation']

        print(self.columnTypeValue)
        print(self.columnTypeValidation)


    def oneToOneAddMappingAndRunBtn_click(self, **event_args):
        if self.oneToOneMappingNameTxtBox.text:
            if anvil.server.call('is_mapping_name_unique', self.user, str(self.oneToOneMappingNameTxtBox.text), app_tables.tb_automation_type_1_2):
                # Execute a test run
                runMapping = anvil.server.call('runMappingTest',
                                                self.user,
                                                self.selectedSourceSheetId,
                                                self.selectedSourceColumnId,
                                                self.selectedDestinationSheetId,
                                                self.selectedDestinationColumnId,
                                                self.columnTypeValue,
                                                self.columnTypeValidation)
    
                if runMapping == 0:
                    if confirm("Great news! Our test run was successful, and we've updated the destination column accordingly. Would you like to proceed by saving and activating this automation?", title="Automation Test: Successful ✅", large=True, dismissible=False):
                        map_activation = True
                    else:
                        map_activation = False
                    
                    saveMapping = anvil.server.call('save_automation',
                                                    map_enabled=map_activation,
                                                    map_name=self.oneToOneMappingNameTxtBox.text,
                                                    map_type=1,
                                                    database=tables.app_tables.tb_automation_type_1_2,
                                                    user_obj=self.user,
                                                    source_sheet_id=self.selectedSourceSheetId,
                                                    source_col_id=self.selectedSourceColumnId,
                                                    source_sheet_name=self.selSrcSheetName,
                                                    source_col_name=self.selSrcColumnName,
                                                    dest_sheet_id=self.selectedDestinationSheetId,
                                                    dest_col_id=self.selectedDestinationColumnId,
                                                    dest_sheet_name=self.selDestSheetName,
                                                    dest_col_name=self.selDestColumnName,
                                                    dest_col_type=self.columnTypeValue,
                                                    dest_col_validation=self.columnTypeValidation)
    
                    if saveMapping:
                        if map_activation:
                            Notification("Success! Your automation was stored and is now live, working behind the scenes to streamline your tasks.", title="Automation Activated 🚀", style="success", timeout=5).show()
                            anvil.open_form('mapperHome')
                        else:
                            Notification(f"All set! We've saved your automation, but it's currently in standby mode. Activate it when you're ready to unleash its potential!", title="Automation Saved (Inactive) 🛌", style="info", timeout=10).show()
                            anvil.open_form('mapperHome')
                    else:
                        Notification(f"Oops! We hit a snag while trying to save your automation. Don't worry, our team is on it. Here's the error detail for the tech-savvy: {saveMapping}", title="Save Error 🚫", style="danger", timeout=10).show()
    
                else:
                    Notification(f"It seems the automation test didn't go as planned. Let's review the settings or check with our support to iron out any issues.", title="Test Unsuccessful ⚠️", style="danger", timeout=10).show()
    
            else:
                Notification(f"Hold on a second! The name '{self.oneToOneMappingNameTxtBox.text}' is already taken. Let's get creative and pick a unique name for this new automation.", title="Name Duplication Alert 📛", style="warning", timeout=10).show()

    

    def oneToOneBackBtn_click(self, **event_args):
        """This method is called when the button is clicked"""
        if self.setup_data:
            anvil.open_form('mapperHome', setup_data=self.setup_data)
        else:
            anvil.open_form('mapperHome')