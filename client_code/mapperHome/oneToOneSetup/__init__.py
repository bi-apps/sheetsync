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
    # def __init__(self, user, **properties):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
      
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
        self.user = anvil.users.get_user()
      
        # Any code you write here will run before the form opens.
        # Get Sheet Names and Id's
        sheet_data = anvil.server.call('getSheetData', self.user)
      
        # Create a dictionary to map sheet names to sheet IDs
        self.sheet_map = {sheet['sheet_name']: sheet['sheet_id'] for sheet in sheet_data}
      
        # Set the dropdown items to be the sheet names
        self.oneToOneSourceSheetDropDown.items = list(self.sheet_map.keys())
        self.oneToOneDestinationSheetDropDown.items = list(self.sheet_map.keys())

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
        """This method is called when the button is clicked"""
        # Is text box filled? if not alert user
        if self.oneToOneMappingNameTxtBox.text:
          # Is the Map name unique? if Not alert user, else Execute Code
          if anvil.server.call('is_mapping_name_unique', self.user, str(self.oneToOneMappingNameTxtBox.text), app_tables.db_sd_one_to_one):
            # Execute a test run
            runMapping = anvil.server.call('runMappingTest',
                                              self.user,
                                              self.selectedSourceSheetId,
                                              self.selectedSourceColumnId,
                                              self.selectedDestinationSheetId,
                                              self.selectedDestinationColumnId,
                                              self.columnTypeValue,
                                              self.columnTypeValidation)
            # Check Test Run Results if not '0' then alert with error else sucess
            if runMapping == 0:
              # Notification("Awsome! Test run successfully completed and destination column was updated with new values", style="success", timeout=2000).show()
              if confirm("The test ran successfully, and the destination column has been updated with the new values. Are you ready to save and activate this Dropdown automation now?", title="Great job! You're a genius, my fellow Smartsheeter! ", large=True, dismissible=False):
                saveMapping = anvil.server.call('saveMapping',
                                                map_enabled=True,
                                                map_name=self.oneToOneMappingNameTxtBox.text,
                                                map_type=1,
                                                database=tables.app_tables.db_sd_one_to_one,
                                                user_obj=self.user,
                                                source_sheet_id=self.selectedSourceSheetId,
                                                source_colum_id=self.selectedSourceColumnId,
                                                source_sheet_name=self.selSrcSheetName,
                                                source_column_name=self.selSrcColumnName,
                                                destination_sheet_id=self.selectedDestinationSheetId,
                                                destination_colum_id=self.selectedDestinationColumnId,
                                                destination_sheet_name=self.selDestSheetName,
                                                destination_column_name=self.selDestColumnName,
                                                destination_colum_type=self.columnTypeValue,
                                                destination_column_validation=self.columnTypeValidation)
                if saveMapping:
                  Notification("Your Dropdown Automation has been saved and activated!", title="Sucess!", style="success", timeout=5).show()
                else:
                  Notification(f"Your Dropdown Automation has not been saved and activated due to Error: {saveMapping}", title="Oops! Error!", style="danger", timeout=10).show()
              else:
                saveMapping = anvil.server.call('saveMapping',
                                map_enabled=True,
                                map_name=self.oneToOneMappingNameTxtBox.text,
                                map_type=1,
                                database=tables.app_tables.db_sd_one_to_one,
                                user_obj=self.user,
                                source_sheet_id=self.selectedSourceSheetId,
                                source_colum_id=self.selectedSourceColumnId,
                                source_sheet_name=self.selSrcSheetName,
                                source_column_name=self.selSrcColumnName,
                                destination_sheet_id=self.selectedDestinationSheetId,
                                destination_colum_id=self.selectedDestinationColumnId,
                                destination_sheet_name=self.selDestSheetName,
                                destination_column_name=self.selDestColumnName,
                                destination_colum_type=self.columnTypeValue,
                                destination_column_validation=self.columnTypeValidation)
              if saveMapping:
                  Notification(f"Your Dropdown Automation has been saved but NOT activated! ", title="Heads Up Fellow Smartsheeter!", style="info", timeout=10).show()
              else:
                  Notification(f"Your Dropdown Automation has not been saved and activated due to Error: {saveMapping}", title="Oops! Error!", style="danger", timeout=10).show()
          else:
              Notification(f"Your Dropdown Automation Test has Failed! Due to Error: {runMapping}", title="Oops! Error! Bail!", style="danger", timeout=10).show()

        else:
            Notification(f"Your Dropdown Automation Name: {self.oneToOneMappingNameTxtBox.text} already Exists, Please Use a Unique Name for every Automation", title="Oops! Not to Creative i see...", style="warning", timeout=10).show()
      
        # anvil.open_form('mapperHome')
        print("error")
      
    def oneToOneBackBtn_click(self, **event_args):
        """This method is called when the button is clicked"""
        anvil.open_form('mapperHome')
        

          

          







          



