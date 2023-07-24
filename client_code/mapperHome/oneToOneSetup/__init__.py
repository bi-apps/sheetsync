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
            runMappingTest = anvil.server.call('testRun',
                                               self.user,
                                               self.selectedSourceSheetId,
                                               self.selectedSourceColumnId,
                                               self.selectedDestinationSheetId,
                                               self.selectedDestinationColumnId,
                                               self.columnTypeValue,
                                               self.columnTypeValidation)
            
            
            alert("Mapping Name Does Not Exist")
          else:
            alert("Mapping Name Exists error")
          
        # if len(self.oneToOneMappingNameTxtBox.text) == 0:
        #     self.oneToOneMappingNameTxtBox.scroll_into_view(smooth=True)
        #     self.oneToOneMappingNameTxtBox.background = app.theme_colors['Invalid Input']
        #     alert("Please choose a mapping name.", title="Mapping Name Empty!" , large=True, dismissible=False)
        # else:
        #     print('source sheet id selected ' + str(self.selectedSourceSheetId))
        #     runMappingTest = anvil.server.call('testRun',self.user, self.selectedSourceSheetId, self.selectedSourceColumnId, self.selectedDestinationSheetId, self.selectedDestinationColumnId, self.columnTypeValue, self.columnTypeValidation)
        #     print(runMappingTest)
        #     if not runMappingTest:
        #       if anvil.server.call('is_mapping_name_unique', self.user, self.oneToOneMappingNameTxtBox.text, app_tables.db_sd_one_to_one):
        #           self.oneToOneAddMappingAndRunBtn.text = 'Sucess! Saved and Enabled'
        #           test = anvil.server.call('saveOneToOneMapping', self)
        #           print(test)
        #           # oneToOneTable = app_tables.db_sd_one_to_one.add_row(user=self.user,
        #           #                                                     src_sheet_name=self.selSrcSheetName,
        #           #                                                     src_sheet_id=self.selectedSourceSheetId,
        #           #                                                     src_sheet_col_name=self.selSrcColumnName,
        #           #                                                     src_sheet_col_id=self.selectedSourceColumnId,
        #           #                                                     dest_sheet_name=self.selDestSheetName,
        #           #                                                     dest_sheet_id=self.selectedDestinationSheetId,
        #           #                                                     dest_col_name=self.selDestColumnName,
        #           #                                                     dest_col_id=self.selectedDestinationColumnId,
        #           #                                                     created_DateStamp=datetime.now(),
        #           #                                                     map_name=self.oneToOneMappingNameTxtBox.text,
        #           #                                                     map_enabled=True,
        #           #                                                     dest_column_type=self.columnTypeValue,
        #           #                                                     dest_column_validation=self.columnTypeValidation)
        
        #           self.oneToOneSourceSheetDropDown.enabled = False
        #           self.oneToOneSourceColumnDropDown.enabled = False
          
        #           self.oneToOneDestinationSheetDropDown.enabled = False
        #           self.oneToOneDestinationColumnDropDown.enabled = False
          
        #           self.oneToOneResetMappingFormBtn.visible = False
        #           self.oneToOneMappingNameTxtBox.enabled = False
        
        #           self.oneToOneAddMappingAndRunBtn.remove_event_handler('click')
        #       else:
        #         self.oneToOneMappingNameTxtBox.scroll_into_view(smooth=True)
        #         self.oneToOneMappingNameTxtBox.background = app.theme_colors['Invalid Input']
        #         alert("Please choose a different mapping name.", title=f"Mapping Name {self.oneToOneMappingNameTxtBox.text} Already Exists" , large=True, dismissible=False)
        #     else:
        #       alert(f"Please review your mapping setup as we've encounted an error while running a test. Error Details : {runMappingTest} and Cannot be of Type {self.columnTypeValue}", title="Mapping Error!" , large=True, dismissible=False)


          








          



