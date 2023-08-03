from ._anvil_designer import criteriaBasedOneToOneSetupTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class criteriaBasedOneToOneSetup(criteriaBasedOneToOneSetupTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Get User
    # self.user = user
    self.user = anvil.users.get_user()

    # # Hide Objects that needs to be hidden on load

    # Get Sheet Names and Id's
    sheet_data = anvil.server.call('getSheetData', self.user)
  
    # Create a dictionary to map sheet names to sheet IDs
    self.sheet_map = {sheet['sheet_name']: sheet['sheet_id'] for sheet in sheet_data}

    # Assigne Sheet names and id's to dropdowns
    self.oneToOneCriteriaBasedSourceSheetDropDown.items = list(self.sheet_map.keys())
    self.oneToOneCriteriaBasedDestinationSheetDropDown.items = list(self.sheet_map.keys())
      
    # Assigne Column Types from database to Destination Colum Types
    self.column_types_data = app_tables.column_types.search()
      
    # Populate the dropdown with 'columnName' values
    self.oneToOneCriteriaBasedDestinationDropdownType.items = [row['column_type'] for row in self.column_types_data]
      
    # Assgne Operator Names and Types to Dropdown
    self.operator_type_data = app_tables.operator_types.search()
      
    # Populate the dropdown with the operator Name Values
    self.oneToOneCriteriaBasedOperatorDropDown.items = [row['operator_names'] for row in self.operator_type_data]

    # ------------- Helper Functions --------------- #
    
  def update_dynamic_source_sheet_dropdown(self):
      selected_source_sheet = self.oneToOneCriteriaBasedSourceSheetDropDown.selected_value
      selected_destination_sheet = self.oneToOneCriteriaBasedDestinationSheetDropDown.selected_value

      if selected_source_sheet and selected_destination_sheet:
         # dynamic_source_sheets = [selected_source_sheet, selected_destination_sheet]
         # self.oneToOneCriteriaBasedDynamicSourceSheetDropDown.items = dynamic_source_sheets
         # self.oneToOneCriteriaBasedDynamicDestinationSheetDropDown.items = dynamic_source_sheets
         # dynamic_source_sheets = [selected_source_sheet, selected_destination_sheet]
         dynamic_source_sheet_list = [selected_source_sheet]
         dynamic_destination_sheet_list = [selected_destination_sheet]
         self.oneToOneCriteriaBasedDynamicSourceSheetDropDown.items = dynamic_source_sheet_list
         self.oneToOneCriteriaBasedDynamicDestinationSheetDropDown.items = dynamic_destination_sheet_list
          
         # self.oneToOneCriteriaBasedDynamicSourceSheetDropDown.selected_value = selected_source_sheet
         # self.oneToOneCriteriaBasedDynamicDestinationSheetDropDown.selected_value = selected_destination_sheet
          
         # self.oneToOneCriteriaBasedDynamicSourceSheetDropDown.enabled = False
         # self.oneToOneCriteriaBasedDynamicDestinationSheetDropDown.enabled = False

         # self.oneToOneCriteriaBasedSourceColumnDropDown.enabled = True
         
      else:
         self.oneToOneCriteriaBasedDynamicSourceSheetDropDown.items = []
         self.oneToOneCriteriaBasedDynamicDestinationSheetDropDown.items = []

    # ------------- Helper Functions End --------------- #

  # ------------- Main Sheet Selection Functions of Screen (Source and Destination Selections) ------------- #
  # Source Sheet Selection Area and Logic
  def oneToOneCriteriaBasedSourceSheetDropDown_change(self, **event_args):
      """This method is called when an item is selected"""
      self.selectedCriteriaSourceSheetName = self.oneToOneCriteriaBasedSourceSheetDropDown.selected_value
    
      if self.selectedCriteriaSourceSheetName is not None:
        self.selectedCriteriaSourceSheetId = self.sheet_map[self.selectedCriteriaSourceSheetName]
        
        # Start Get Columns ----------------------------------------------------------------
        # Set Dropdown Source Coulmn State and Values
        self.oneToOneCriteriaBasedSourceColumnDropDown.enabled = True
        # Get Column Names for Selected Sheet and Insert Values into Dropdown
        columns_data = anvil.server.call('getColumnNames',self.selectedCriteriaSourceSheetId, self.user)
        self.column_map = {column['title']: column['id'] for column in columns_data}
        self.oneToOneCriteriaBasedSourceColumnDropDown.items = list(self.column_map.keys())
        
        # ------- Handel Selected Type's Logic of Display ------- #
        self.oneToOneCriteriaSourceSheetText.text = self.selectedCriteriaSourceSheetName
        self.oneToOneCriteriaBasedCiteriaColumnDropDown.items = list(self.column_map.keys()) 
        
        # Update dynamic source sheet dropdown
        self.update_dynamic_source_sheet_dropdown()
          
        # End Get Columns ----------------------------------------------------------------
        print(f"Selected One To One Criteria Based Source Sheet ID: {self.selectedCriteriaSourceSheetId}")
  # Destination Sheet Selection Area and Logic
  def oneToOneCriteriaBasedDestinationSheetDropDown_change(self, **event_args):
      """This method is called when an item is selected"""
      self.selectedCriteriaDestinationSheetName = self.oneToOneCriteriaBasedDestinationSheetDropDown.selected_value
      if self.selectedCriteriaDestinationSheetName is not None:
        self.selectCriteriaBasedDestinationSheetId = self.sheet_map[self.selectedCriteriaDestinationSheetName]

        # Start Get Columns ----------------------------------------------------------------
        # Set Dropdown Source Coulmn State and Values
        self.oneToOneCriteriaBasedDestinationColumnDropDown.enabled = True
        # Get Column Names for Selected Sheet and Insert Values into Dropdown
        columns_data = anvil.server.call('getColumnNames',self.selectCriteriaBasedDestinationSheetId, self.user)
        self.column_map = {column['title']: column['id'] for column in columns_data}
        self.oneToOneCriteriaBasedDestinationColumnDropDown.items = list(self.column_map.keys())
        # End Get Columns ----------------------------------------------------------------
        
        # Update dynamic source sheet dropdown
        self.update_dynamic_source_sheet_dropdown()
          
        print(f"Selected One To One Criteria Based Destination Sheet ID: {self.selectCriteriaBasedDestinationSheetId}")
  # Ensure all selections are made before allowing criterion selection dropdown
  def oneToOneCriteriaBasedDestinationColumnDropDown_change(self, **event_args):
      """This method is called when an item is selected"""
      self.selectCriteriaBasedDestinationColumnType = self.oneToOneCriteriaBasedDestinationColumnDropDown.selected_value
      if self.selectCriteriaBasedDestinationColumnType is not None:
        self.oneToOneCriteriaBasedDestinationDropdownType.enabled = True
  # Criteria Dropdown Change Logic between Logical / Dynamic Criteria Forms
  def oneToOneCriteriaTypeDropDown_change(self, **event_args):
      """This method is called when an item is selected"""
      selectedValue = self.oneToOneCriteriaTypeDropDown.selected_value
      if selectedValue is not None:
        if selectedValue == "Logical":
          # ------- Handel Displaying Between selected Criteria Type ------- #
          self.oneToOneCriteriaDynamicFlowPanel.visible = False
          self.oneToOneCriteriaLogicalFlowPanel.visible = True
        elif selectedValue == "Dynamic":
          # ------- Handel Displaying Between selected Criteria Type ------- #
          self.oneToOneCriteriaLogicalFlowPanel.visible = False
          self.oneToOneCriteriaDynamicFlowPanel.visible = True
      else:
        self.oneToOneCriteriaLogicalFlowPanel.visible = False
        self.oneToOneCriteriaDynamicFlowPanel.visible = False
          
          
  # ----------- Dynamic Criterion Section ------------- #
  # Dynamic
  def oneToOneCriteriaBasedDynamicSourceSheetDropDown_change(self, **event_args):
      """This method is called when an item is selected"""
      self.selectDynamicSourceSheetName = self.oneToOneCriteriaBasedDynamicSourceSheetDropDown.selected_value

      if self.selectDynamicSourceSheetName is not None:
        self.selectDynamicSourceSheetId = self.sheet_map[self.selectDynamicSourceSheetName]

        # Start Get Columns ----------------------------------------------------------------
        # Set Dropdown Source Coulmn State and Values
        self.oneToOneCriteriaBasedDynamicSourceColumnDropDown.enabled = True
        # Get Column Names for Selected Sheet and Insert Values into Dropdown
        columns_data = anvil.server.call('getColumnNames',self.selectDynamicSourceSheetId, self.user)
        self.column_map = {column['title']: column['id'] for column in columns_data}
        self.oneToOneCriteriaBasedDynamicSourceColumnDropDown.items = list(self.column_map.keys())
  # Dynamic
  def oneToOneCriteriaBasedDynamicSourceColumnDropDown_change(self, **event_args):
      """This method is called when an item is selected"""
      pass
  # Dynamic
  def oneToOneCriteriaBasedDynamicDestinationSheetDropDown_change(self, **event_args):
      """This method is called when an item is selected"""
      self.selectDynamicDestinationSheetName = self.oneToOneCriteriaBasedDynamicDestinationSheetDropDown.selected_value

      if self.selectDynamicDestinationSheetName is not None:
        self.selectDynamicDestinationSheetId = self.sheet_map[self.selectDynamicDestinationSheetName]

        # Start Get Columns ----------------------------------------------------------------
        # Set Dropdown Source Coulmn State and Values
        self.oneToOneCriteriaBasedDynamicDestinationColumnDropDown.enabled = True
        # Get Column Names for Selected Sheet and Insert Values into Dropdown
        columns_data = anvil.server.call('getColumnNames',self.selectDynamicDestinationSheetId, self.user)
        self.column_map = {column['title']: column['id'] for column in columns_data}
        self.oneToOneCriteriaBasedDynamicDestinationColumnDropDown.items = list(self.column_map.keys())
          
          
  # ----------- Logical Criterion Section --------------#
  # Logical
  def oneToOneCriteriaBasedOperatorDropDown_change(self, **event_args):
      """This method is called when an item is selected"""
      self.selectedOperatorName = self.oneToOneCriteriaBasedOperatorDropDown.selected_value
      selected_row = next((row for row in self.operator_type_data if row['operator_names'] == self.selectedOperatorName), None)

      if self.selectedOperatorName is not None:
         self.selectedOperatorValue = selected_row['operator_keywords']

         # If Operator is Equals to, Not Equals to Or Contains display Value input else do not display value input
         if self.selectedOperatorValue in ["==", "!=", "in"]:
           self.oneToOneCriteriaLogicalValue.visible = True
         else:
           self.oneToOneCriteriaLogicalValue.visible = False

         if self.selectedOperatorValue in ["not in", "select_included*"]:
           self.oneToOneCriteriaBasedOperatorIsOneOfOrNotLinearPanel.visible = True
           self.oneToOneCriteriaBasedOperatorIsOneOfOrNotLabel.text = "These Values"
             
           # Last Busy Here!
           logical_criteria_columns_data = anvil.server.call('getColumnNames',self.selectedCriteriaSourceSheetId, self.user)
           self.logical_criteria_column_map = {column['title']: column['id'] for column in logical_criteria_columns_data}
      
           self.selectLogicalCriterionColumnId = self.logical_criteria_column_map[self.oneToOneCriteriaBasedCiteriaColumnDropDown.selected_value]
           self.column_row_values = anvil.server.call('getColumnData', self.user, self.selectedCriteriaSourceSheetId, self.selectLogicalCriterionColumnId )
           print(self.column_row_values)
           self.oneToOneCriteriaBasedOperatorIsOneOfOrNotDropdown.items = self.column_row_values # Set Drop down values of columns rows in sheet
             
         else:
           self.oneToOneCriteriaBasedOperatorIsOneOfOrNotLinearPanel.visible = False

         if self.selectedOperatorValue in ['range*']:
           self.oneToOneCriteriaLogicalFromValue.visible = True
           self.oneToOneCriteriaLogicalToValue.visible = True
         else:
           self.oneToOneCriteriaLogicalFromValue.visible = False
           self.oneToOneCriteriaLogicalToValue.visible = False
             
      else:
         self.oneToOneCriteriaLogicalValue.visible = False
        

         print(self.selectedOperatorValue)