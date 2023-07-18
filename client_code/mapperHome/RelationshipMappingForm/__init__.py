from ._anvil_designer import RelationshipMappingFormTemplate
from anvil import FlowPanel
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from functools import partial

# Rest of your code...

class RelationshipMappingForm(RelationshipMappingFormTemplate):
    def __init__(self, **properties):
        super().__init__(**properties)
        
        self.source_sheets = [{'sheet_id': '1', 'sheet_name': 'Source Sheet 1'}, {'sheet_id': '2', 'sheet_name': 'Source Sheet 2'}, {'sheet_id': '3', 'sheet_name': 'Source Sheet 3'}]
        self.source_sheet_dropdown = DropDown(items=[sheet['sheet_name'] for sheet in self.source_sheets])
        self.source_column_dropdown = DropDown()
        
        self.destination_mappings = []
        
        self.add_destination_button = Button(text="Add Destination", icon="fa:plus", role="secondary")
        self.add_destination_button.set_event_handler('click', self.add_destination)
        
        # Create a FlowPanel for the source sheet, source column, and add destination button
        self.source_panel = FlowPanel()  # Define self.source_panel as an instance attribute
        self.source_panel.add_component(self.source_sheet_dropdown)
        self.source_panel.add_component(self.source_column_dropdown)
        self.source_panel.add_component(self.add_destination_button)
        
        self.add_component(self.source_panel)
        
        self.source_sheet_dropdown.set_event_handler('change', self.update_source_columns)
        self.source_column_dropdown.set_event_handler('change', self.handle_source_selection)
        
        
    def apply_flow_layout(self, **event_args):
        self.column_panel.get_dom_node().classList.add("flow-layout")  # Apply the "flow-layout" CSS class to the panel
        
    def update_source_columns(self, **event_args):
        selected_sheet = self.source_sheet_dropdown.selected_value
        # Perform logic to retrieve the columns for the selected sheet
        # Update self.source_column_dropdown with the retrieved columns
        columns = ['Column 1', 'Column 2', 'Column 3']  # Replace with the actual columns
        self.source_column_dropdown.items = columns
    
    def handle_source_selection(self, **event_args):
        selected_column = self.source_column_dropdown.selected_value
        if selected_column:
            self.add_destination_button.visible = True
        else:
            self.add_destination_button.visible = False
    
    def add_destination(self, **event_args):
        destination_sheet_dropdown = DropDown()
        destination_column_dropdown = DropDown()
        remove_destination_button = Button(text="", icon="fa:trash", role="secondary", align="center")
    
        destination_mapping = {
            'sheet_dropdown': destination_sheet_dropdown,
            'column_dropdown': destination_column_dropdown,
            'remove_button': remove_destination_button,
            'panel': None  # Add a placeholder for the panel reference
        }
        self.destination_mappings.append(destination_mapping)

        destination_panel = FlowPanel()
        destination_panel.add_component(Label(text="Destination Sheet"))
        destination_panel.add_component(destination_sheet_dropdown)
        destination_panel.add_component(Label(text="Destination Column"))
        destination_panel.add_component(destination_column_dropdown)
        destination_panel.add_component(remove_destination_button)
        
        self.source_panel.add_component(destination_panel)  # Add the destination_panel to the self.source_panel
        
        
        destination_mapping['panel'] = destination_panel  # Store the reference to the panel
      
        remove_destination_button.set_event_handler('click', partial(self.remove_destination, destination_mapping))

        # Set the CSS properties to achieve the desired layout
        destination_panel.set_css_property("display", "flex")
        destination_panel.set_css_property("flex-direction", "column")
        destination_sheet_dropdown.set_css_property("margin-right", "5px")
        destination_column_dropdown.set_css_property("margin-right", "5px")
  
    def remove_destination(self, destination_mapping, **event_args):
        self.destination_mappings.remove(destination_mapping)
        destination_mapping['panel'].remove_from_parent()

# Rest of your code...
