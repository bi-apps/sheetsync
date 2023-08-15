from ._anvil_designer import ItemTemplate5Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate5(ItemTemplate5Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.user = anvil.users.get_user()
        
        # Set the initial appearance of the onOffAutomationBtn based on its text
        if self.onOffAutomationBtn.text == "ON":
            self.onOffAutomationBtn.background = "#4CAF50"  # Green color
        else:
            self.onOffAutomationBtn.background = "#F44336"  # Red color

        # Any code you write here will run before the form opens.

    def runAutomationBtn_click(self, **event_args):
        """This method is called when the button is clicked"""
        selected_automation = self.runAutomationBtn.tag
        print(f"Clicked Run Button : {self.editAutomationBtn.tag['map_type']}")

    def editAutomationBtn_click(self, **event_args):
        """This method is called when the button is clicked"""
        selected_automation = self.editAutomationBtn.tag
        if selected_automation['map_type'] == 1:
            print(f"Sending {selected_automation['map_name']} to One to One Setup Form with ID : {self.item.get_id()}")
            
            edit_data = {
                "row" : selected_automation,
                "row_id" : self.item.get_id()
            }
            open_form('mapperHome.oneToOneSetup', edit_data = edit_data)
        elif selected_automation['map_type'] == 2:
            edit_data = {
                "row" : selected_automation,
                "row_id" : self.item.get_id()
            }
            print(f"Sending {selected_automation['map_name']} to Criteria Based One to One Setup Form")
            open_form('mapperHome.criteriaBasedOneToOneSetup', edit_data = edit_data)
        
        print(f"Clicked Edit Button : {self.editAutomationBtn.tag['map_name']}")

    def onOffAutomationBtn_click(self, **event_args):
        """This method is called when the button is clicked"""
        button = self.onOffAutomationBtn
        
        # Toggle the state of the button and update the database
        if button.text == "ON":
            button.text = "OFF"
            self.onOffAutomationLable.text = "inactive"
            button.background = "#F44336"  # Red color
            button.tag['map_enabled'] = False
        else:
            button.text = "ON"
            self.onOffAutomationLable.text = "Active"
            button.background = "#4CAF50"  # Green color
            button.tag['map_enabled'] = True
        
        # Update the database with the new value
        anvil.server.call('update_map_enabled', button.tag['map_name'], button.tag['map_enabled'], self.user)
        print(f"Clicked ON/OFF Button : {button.tag['map_enabled']}")

    def deleteAutomationBtn_click(self, **event_args):
        """This method is called when the button is clicked"""
        row_to_delete = self.item.get_id()
        delete_row = anvil.server.call('delete_automation',
                                      row_id = row_to_delete,
                                      user = self.user)
        if delete_row:
            open_form('listAutomations')








