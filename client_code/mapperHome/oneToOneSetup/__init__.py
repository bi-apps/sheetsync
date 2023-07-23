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
        self.user = anvil.users.get_user()
      
        # Any code you write here will run before the form opens.
        # Get Sheet Names and Id's
        sheet_data = anvil.server.call('getSheetData', self.user)
      
        # Create a dictionary to map sheet names to sheet IDs
        self.sheet_map = {sheet['sheet_name']: sheet['sheet_id'] for sheet in sheet_data}
      
        # Set the dropdown items to be the sheet names
        self.oneToOneSourceSheetDropDown.items = list(self.sheet_map.keys())
        self.oneToOneDestinationSheetDropDown.items = list(self.sheet_map.keys())

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
            columns_data = anvil.server.call('getSheetColumn',self.selectedSourceSheetId, self.user)
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
            self.selectSourceColumnId = self.column_map[self.selSrcColumnName]
            self.oneToOneDestinationSheetCard.visible = True
            # Enable Filter Image
            self.oneToOneFilterImageObject.visible = True

        print(f"Selected Source Column ID: {self.selectSourceColumnId}")

    def oneToOneDestinationSheetDropDown_change(self, **event_args):
        """This method is called when an item is selected"""
        self.selDestSheetName = self.oneToOneDestinationSheetDropDown.selected_value

        if self.selDestSheetName is not None:
          self.selectedDestinationSheetId = self.sheet_map[self.selDestSheetName]

          # Start Get Columns ----------------------------------------------------------------
          # Set Dropdown Source Coulmn State and Values
          self.oneToOneDestinationColumnDropDown.enabled = True
          # Get Column Names for Selected Sheet and Insert Values into Dropdown
          columns_data = anvil.server.call('getSheetColumn',self.selectedDestinationSheetId, self.user)
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

    def oneToOneAddMappingAndRunBtn_click(self, **event_args):
        """This method is called when the button is clicked"""
        # createdDateTimeStamp = datetime.now(anvil.tz.tzlocal())
        oneToOneTable = app_tables.db_sd_one_to_one.add_row(user=self.user,
                                                            src_sheet_name=self.selSrcSheetName,
                                                            src_sheet_id=self.selectedSourceSheetId,
                                                            src_sheet_col_name=self.selSrcColumnName,
                                                            src_sheet_col_id=self.selectedDestinationColumnId,
                                                            dest_sheet_name=self.selDestSheetName,
                                                            dest_sheet_id=self.selectedDestinationSheetId,
                                                            dest_col_name=self.selDestColumnName,
                                                            dest_col_id=self.selectedDestinationColumnId,
                                                            created_DateStamp=datetime.now(),
                                                            map_name=self.oneToOneMappingNameTxtBox.text)

        anvil.server.call('getColumnData',self.selectedSourceSheetId, self.selectSourceColumnId, self.user)


          



