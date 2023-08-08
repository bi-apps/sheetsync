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

    self.user = anvil.users.get_user()

    # # Hide Objects that needs to be hidden on load
    self.oneToOneCriteriaBasedMultiSelectDropDown.visible = False

    # Get Sheet Names and Id's
    get_sheet_names_and_ids = anvil.server.call('getSheetData', self.user)
  
    # Create a dictionary to map sheet names to sheet IDs
    self.sheet_name_and_ids_map = {sheet['sheet_name']: sheet['sheet_id'] for sheet in get_sheet_names_and_ids}

    # Assigne Sheet names and id's to dropdowns
    self.oneToOneCriteriaBasedSourceSheetDropDown.items = list(self.sheet_name_and_ids_map.keys()) # This is the Source Sheet DropDown Items Initiation
    self.oneToOneCriteriaBasedDestinationSheetDropDown.items = list(self.sheet_name_and_ids_map.keys()) # This is the Destination Sheet DropDown Items Initiation
      
    # Assigne Column Types from database to Destination Colum Types
    self.db_column_type_data = app_tables.column_types.search()
      
    # Populate the dropdown with 'columnName' values
    self.oneToOneCriteriaBasedDestinationDropdownType.items = [row['column_type'] for row in self.db_column_type_data] # This is the Destination Columns Type i.e Single Dropdown Initiations
      
    # Assgne Operator Names and Types to Dropdown
    self.db_citeria_operators_data = app_tables.operator_types.search()
      
    # Populate the dropdown with the operator Name Values
    self.oneToOneCriteriaBasedOperatorDropDown.items = [row['operator_names'] for row in self.db_citeria_operators_data] # This is the Citeria logical Operator Type DropDown i.e == or !=

    # ------------- Helper Functions --------------- #
    
  def update_dynamic_source_sheet_dropdown(self):
      selected_source_sheet_name = self.oneToOneCriteriaBasedSourceSheetDropDown.selected_value # (Source) This is for The Dynamic Criterion Only, Allows a user to select the source or destination sheet Only
      selected_destination_sheet_name = self.oneToOneCriteriaBasedDestinationSheetDropDown.selected_value # (Destination) This is for The Dynamic Criterion Only, Allows a user to select the source or destination sheet Only

      if selected_source_sheet_name and selected_destination_sheet_name:

         dynamic_source_sheet_list = [selected_source_sheet_name]
         dynamic_destination_sheet_list = [selected_destination_sheet_name]
         self.oneToOneCriteriaBasedDynamicSourceSheetDropDown.items = dynamic_source_sheet_list # Initiate the DropDown Items based on the selected source sheet
         self.oneToOneCriteriaBasedDynamicDestinationSheetDropDown.items = dynamic_destination_sheet_list # Initiate the DropDown Items based on the selected Destination sheet

      else:
         self.oneToOneCriteriaBasedDynamicSourceSheetDropDown.items = []
         self.oneToOneCriteriaBasedDynamicDestinationSheetDropDown.items = []

    # ------------- Helper Functions End --------------- #


    
  # ------------- Main Sheet Selection Functions of Screen (Source and Destination Selections) ------------- #
  # Source Sheet Selection Area and Logic
  def oneToOneCriteriaBasedSourceSheetDropDown_change(self, **event_args):
      """This method is called when an item is selected"""
      self.selected_criteria_source_sheet_name = self.oneToOneCriteriaBasedSourceSheetDropDown.selected_value
    
      if self.selected_criteria_source_sheet_name is not None:
        self.selected_criteria_source_sheet_id = self.sheet_name_and_ids_map[self.selected_criteria_source_sheet_name]
        
        # Start Get Columns ----------------------------------------------------------------
        # Set Dropdown Source Coulmn State and Values
        self.oneToOneCriteriaBasedSourceColumnDropDown.enabled = True
        # Get Column Names for Selected Sheet and Insert Values into Dropdown
        get_columns_data_based_on_sheet_id = anvil.server.call('getColumnNames',self.selected_criteria_source_sheet_id, self.user)
        self.column_name_and_ids_map = {column['title']: column['id'] for column in get_columns_data_based_on_sheet_id}
        self.oneToOneCriteriaBasedSourceColumnDropDown.items = list(self.column_name_and_ids_map.keys())
        
        # ------- Handel Selected Type's Logic of Display ------- #
        self.oneToOneCriteriaSourceSheetText.text = self.selected_criteria_source_sheet_name # This will add the selected Source Sheet as the Default Value in the Logical Criteia Source Sheet Name
        self.oneToOneCriteriaBasedCiteriaColumnDropDown.items = list(self.column_name_and_ids_map.keys()) # This will add the selected source sheet Column Names to the Logical Criteria Columns DropDown
        
        # Update dynamic source sheet dropdown
        self.update_dynamic_source_sheet_dropdown()
          
        # End Get Columns ----------------------------------------------------------------
        print(f"Selected One To One Criteria Based Source Sheet ID: {self.selected_criteria_source_sheet_id}")

    
  def oneToOneCriteriaBasedSourceColumnDropDown_change(self, **event_args):
      """This method is called when an item is selected"""
      self.selected_criteria_source_column_name = self.oneToOneCriteriaBasedSourceColumnDropDown.selected_value
      if self.selected_criteria_source_column_name is not None:
          self.selected_criteria_source_column_id = self.column_name_and_ids_map[self.selected_criteria_source_column_name]
          
      print(f"Selected Source Column ID: {self.selected_criteria_source_column_id}")

    
  # Destination Sheet Selection Area and Logic
  def oneToOneCriteriaBasedDestinationSheetDropDown_change(self, **event_args):
      """This method is called when an item is selected"""
      self.selected_criteria_destination_sheet_name = self.oneToOneCriteriaBasedDestinationSheetDropDown.selected_value
      if self.selected_criteria_destination_sheet_name is not None:
        self.selected_criteria_destination_sheet_id = self.sheet_name_and_ids_map[self.selected_criteria_destination_sheet_name]

        # Start Get Columns ----------------------------------------------------------------
        # Set Dropdown Source Coulmn State and Values
        self.oneToOneCriteriaBasedDestinationColumnDropDown.enabled = True
        # Get Column Names for Selected Sheet and Insert Values into Dropdown
        get_columns_data_based_on_sheet_id = anvil.server.call('getColumnNames',self.selected_criteria_destination_sheet_id, self.user)
        self.column_name_and_ids_map = {column['title']: column['id'] for column in get_columns_data_based_on_sheet_id}
        self.oneToOneCriteriaBasedDestinationColumnDropDown.items = list(self.column_name_and_ids_map.keys())
        # End Get Columns ----------------------------------------------------------------
        
        # Update dynamic source sheet dropdown
        self.update_dynamic_source_sheet_dropdown()
          
        print(f"Selected One To One Criteria Based Destination Sheet ID: {self.selected_criteria_destination_sheet_id}")

    

  def oneToOneCriteriaBasedDestinationColumnDropDown_change(self, **event_args):
      """This method is called when an item is selected"""
      self.selected_criteria_destination_column_type_name = self.oneToOneCriteriaBasedDestinationColumnDropDown.selected_value
      if self.selected_criteria_destination_column_type_name is not None:
        self.selected_criteria_destination_column_id = self.column_name_and_ids_map[self.selected_criteria_destination_column_type_name]
        self.oneToOneDestinationColumnTypeLinearPanel.visible = True
        self.oneToOneCriteriaBasedDestinationDropdownType.enabled = True
          
      print(f"Selected Source Column ID: {self.selected_criteria_destination_column_id}")

    

  def oneToOneCriteriaBasedDestinationDropdownType_change(self, **event_args):
      """This method is called when an item is selected"""
      self.selected_column_type_name = self.oneToOneCriteriaBasedDestinationDropdownType.selected_value
      selected_column_type_row = next((row for row in self.db_column_type_data if row['column_type'] == self.selected_column_type_name), None)
      
      if self.selected_column_type_name:
        self.selected_destination_column_type_value = selected_column_type_row['column_type_value']
        self.selected_destination_column_validation_type = selected_column_type_row['column_type_validation']
        self.oneToOneCriteriaTypeDropDown.enabled = True

      print(self.selected_destination_column_type_value)
      print(self.selected_destination_column_validation_type)
      
    
  # Criteria Dropdown Change Logic between Logical / Dynamic Criteria Forms
  def oneToOneCriteriaTypeDropDown_change(self, **event_args):
      """This method is called when an item is selected"""
      self.selected_criterion_type = self.oneToOneCriteriaTypeDropDown.selected_value
      
      if self.selected_criterion_type is not None:
        if self.selected_criterion_type == "Logical":
          # ------- Handel Displaying Between selected Criteria Type ------- #
          self.oneToOneCriteriaDynamicFlowPanel.visible = False
          self.oneToOneCriteriaLogicalFlowPanel.visible = True
            
        elif self.selected_criterion_type == "Dynamic":
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
      self.selected_dynamic_source_sheet_name = self.oneToOneCriteriaBasedDynamicSourceSheetDropDown.selected_value

      if self.selected_dynamic_source_sheet_name is not None:
        self.selected_dynamic_source_sheet_id = self.sheet_name_and_ids_map[self.selected_dynamic_source_sheet_name]

        # Start Get Columns ----------------------------------------------------------------
        # Set Dropdown Source Coulmn State and Values
        self.oneToOneCriteriaBasedDynamicSourceColumnDropDown.enabled = True
        # Get Column Names for Selected Sheet and Insert Values into Dropdown
        get_columns_data_based_on_sheet_id = anvil.server.call('getColumnNames',self.selected_dynamic_source_sheet_id, self.user)
        self.column_name_and_ids_map = {column['title']: column['id'] for column in get_columns_data_based_on_sheet_id}
        self.oneToOneCriteriaBasedDynamicSourceColumnDropDown.items = list(self.column_name_and_ids_map.keys())

      print(f"selected_dynamic_source_sheet_id: {self.selected_dynamic_source_sheet_id}")

  # Dynamic
  def oneToOneCriteriaBasedDynamicSourceColumnDropDown_change(self, **event_args):
      """This method is called when an item is selected"""
      self.selected_dynamic_source_column_name = self.oneToOneCriteriaBasedDynamicSourceColumnDropDown.selected_value
      if self.selected_dynamic_source_column_name is not None:
          self.selected_dynamic_source_column_id = self.column_name_and_ids_map[self.selected_dynamic_source_column_name]
          
      print(f"selected_dynamic_source_column_id: {self.selected_dynamic_source_column_id}")
      # pass
  # Dynamic

  def oneToOneCriteriaBasedDynamicDestinationSheetDropDown_change(self, **event_args):
      """This method is called when an item is selected"""
      self.selected_dynamic_destination_sheet_name = self.oneToOneCriteriaBasedDynamicDestinationSheetDropDown.selected_value

      if self.selected_dynamic_destination_sheet_name is not None:
        self.selected_dynamic_destination_sheet_id = self.sheet_name_and_ids_map[self.selected_dynamic_destination_sheet_name]

        # Start Get Columns ----------------------------------------------------------------
        # Set Dropdown Source Coulmn State and Values
        self.oneToOneCriteriaBasedDynamicDestinationColumnDropDown.enabled = True
        # Get Column Names for Selected Sheet and Insert Values into Dropdown
        get_columns_data_based_on_sheet_id = anvil.server.call('getColumnNames',self.selected_dynamic_destination_sheet_id, self.user)
        self.column_name_and_ids_map = {column['title']: column['id'] for column in get_columns_data_based_on_sheet_id}
        self.oneToOneCriteriaBasedDynamicDestinationColumnDropDown.items = list(self.column_name_and_ids_map.keys())

      print(f"selected_dynamic_destination_sheet_id: {self.selected_dynamic_destination_sheet_id}")

  def oneToOneCriteriaBasedDynamicDestinationColumnDropDown_change(self, **event_args):
      """This method is called when an item is selected"""
      self.selected_dynamic_destination_column_name = self.oneToOneCriteriaBasedDynamicDestinationColumnDropDown.selected_value
      if self.selected_dynamic_destination_column_name is not None:
          self.selected_dynamic_destination_column_id = self.column_name_and_ids_map[self.selected_dynamic_destination_column_name]

      print(f"selected_dynamic_destination_column_id: {self.selected_dynamic_destination_column_id}")



#########    LAST HERE DERICK    ##########
  # ----------- Logical Criterion Section --------------#
  # Logical
  def oneToOneCriteriaBasedOperatorDropDown_change(self, **event_args):
    """This method is called when an item is selected"""
    self.selected_operator_name = self.oneToOneCriteriaBasedOperatorDropDown.selected_value
    selected_operator_row = next((row for row in self.db_citeria_operators_data if row['operator_names'] == self.selected_operator_name), None)

    # Define visibility sets
    single_value_elements = [self.oneToOneCriteriaLogicalValue]
    range_value_elements = [self.oneToOneCriteriaLogicalFromValue, self.oneToOneCriteriaLogicalToValue]
    list_value_elements = [self.oneToOneCriteriaBasedMultiSelectDropDown]

    # Hide all elements by default
    for elem in single_value_elements + range_value_elements + list_value_elements:
        elem.visible = False

    if selected_operator_row:
        self.selected_operator_values = selected_operator_row['operator_keywords']
        print(self.selected_operator_values)

        operator_ui_behavior = {
            "==": single_value_elements,
            "!=": single_value_elements,
            "contains": single_value_elements,
            "is_one_of": list_value_elements,
            "is_not_one_of": list_value_elements,
            "between": range_value_elements
        }

        # Show elements based on operator
        for elem in operator_ui_behavior.get(self.selected_operator_values, []):
            elem.visible = True

        # Additional behavior for list_value_elements
        if self.selected_operator_values in ["is_one_of", "is_not_one_of"]:
             # self.oneToOneCriteriaBasedOperatorIsOneOfOrNotLabel.text = "These Values"
             self.oneToOneCriteriaBasedMultiSelectDropDown
             logical_criteria_columns_data = anvil.server.call('getColumnNames', self.selected_criteria_source_sheet_id, self.user)
             self.logical_criteria_column_map = {column['title']: column['id'] for column in logical_criteria_columns_data}
            
             self.selected_logical_criterion_column_id = self.logical_criteria_column_map[self.oneToOneCriteriaBasedCiteriaColumnDropDown.selected_value]
            
             self.logical_criterion_row_values = anvil.server.call('getColumnData', self.user, self.selected_criteria_source_sheet_id, self.selected_logical_criterion_column_id)
             self.oneToOneCriteriaBasedMultiSelectDropDown.items = self.logical_criterion_row_values
             

        if self.selected_operator_values in ["==", "!="]:
             logical_criteria_columns_data = anvil.server.call('getColumnNames', self.selected_criteria_source_sheet_id, self.user)
             self.logical_criteria_column_map = {column['title']: column['id'] for column in logical_criteria_columns_data}
            
             self.selected_logical_criterion_column_id = self.logical_criteria_column_map[self.oneToOneCriteriaBasedCiteriaColumnDropDown.selected_value]
            
             self.logical_criterion_row_values = anvil.server.call('getColumnData', self.user, self.selected_criteria_source_sheet_id, self.selected_logical_criterion_column_id)
             self.oneToOneCriteriaBasedEqualsToDropDown.items = self.logical_criterion_row_values

  def oneToOneCriteriaBasedCiteriaColumnDropDown_change(self, **event_args):
     """This method is called when an item is selected"""
     self.oneToOneCriteriaBasedOperatorDropDown_change()

  def oneToOneCriteriaBasedEqualsToDropDown_change(self, **event_args):
      """This method is called when an item is selected"""
      self.criterion_value_selected = self.oneToOneCriteriaBasedEqualsToDropDown.selected_value


  def oneToOneCriteriaBasedRunMappingBtn_click(self, **event_args):
      """This method is called when the button is clicked"""
      """Remember i am focusing on testing the logical criterion first the below is not dynamic nor scalible!!!!"""
      
      if self.oneToOneCriteriaBasedMultiSelectDropDown.selected_tokens is not None:
          self.criterion_value_selected = self.oneToOneCriteriaBasedMultiSelectDropDown.selected_tokens
      if self.oneToOneCriteriaBasedEqualsToDropDown.selected_value is not None:
          self.criterion_value_selected = self.oneToOneCriteriaBasedEqualsToDropDown.selected_value
          
      print(self.oneToOneCriteriaBasedMultiSelectDropDown.selected_tokens)
      doWe = anvil.server.call('houstonWeHaveAProblem',
                              user_id = self.user,
                              selected_source_sheet_id = self.selected_criteria_source_sheet_id,
                              selected_source_sheet_column_id = self.selected_criteria_source_column_id,
                              
                              selected_destination_sheet_id = self.selected_criteria_destination_sheet_id,
                              selected_destination_sheet_column_id = self.selected_criteria_destination_column_id,
                              
                              selected_destination_column_type_value = self.selected_destination_column_type_value,
                              selected_destination_column_validation = self.selected_destination_column_validation_type,
                              
                              selected_criteria_type = self.selected_criterion_type,
                              
                              selected_criteria_source_sheet_id = self.selected_criteria_source_sheet_id,
                              selected_criteria_source_column_id = self.selected_logical_criterion_column_id,
                               
                              selected_criteria_operator = self.selected_operator_values,
                               
                              selected_criteria_value = self.criterion_value_selected)
      # print(doWe)








      






            