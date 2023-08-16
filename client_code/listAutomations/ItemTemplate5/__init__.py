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
        if selected_automation['map_type'] == 1:
            run_test = anvil.server.call('runMappingTest',
                                                    self.user,
                                                    selected_automation['src_sheet_id'],
                                                    selected_automation['src_sheet_col_id'],
                                                    selected_automation['dest_sheet_id'],
                                                    selected_automation['dest_sheet_col_id'],
                                                    selected_automation['dest_sheet_col_type'],
                                                    selected_automation['dest_sheet_col_validation'])

            if run_test == 0:
                Notification(f"The automation ran on-demand successfully! Your data has been updated. If you encounter any discrepancies, please review your settings or contact support.", 
                            title="On-Demand Run Successful ✅", 
                            style="success", 
                            timeout=10).show()
            elif run_test != 0:
                Notification(f"Oops! The on-demand automation run faced an issue. Please review your settings, or contact support for assistance. Error Code: {do_we_really}", 
                            title="On-Demand Run Failed ⚠️", 
                            style="danger", 
                            timeout=10).show()

        if selected_automation['map_type'] == 2:
            
            do_we_really = anvil.server.call('houstonWeHaveAProblem',
                                            user_id=self.user,
                                            selected_source_sheet_id=selected_automation['src_sheet_id'],
                                            selected_source_sheet_column_id=selected_automation['src_sheet_col_id'],
    
                                            selected_destination_sheet_id=selected_automation['dest_sheet_id'],
                                            selected_destination_sheet_column_id=selected_automation['dest_sheet_col_id'],
    
                                            selected_destination_column_type_value=selected_automation['dest_sheet_col_type'],
                                            selected_destination_column_validation=selected_automation['dest_sheet_col_validation'],
        
                                            selected_criteria_type=selected_automation['criterion_type'],
        
                                            selected_criteria_source_sheet_id=selected_automation['criterion_src_sheet_id'],
                                            selected_criteria_source_column_id=selected_automation['criterion_src_sheet_col_id'],
        
                                            selected_criteria_operator=selected_automation['criterion_operator_type_value'],
        
                                            selected_criteria_value=selected_automation['criterion_value'])
            if do_we_really == 0:
                Notification(f"The automation ran on-demand successfully! Your data has been updated. If you encounter any discrepancies, please review your settings or contact support.", 
                            title="On-Demand Run Successful ✅", 
                            style="success", 
                            timeout=10).show()
            elif do_we_really != 0:
                Notification(f"Oops! The on-demand automation run faced an issue. Please review your settings, or contact support for assistance. Error Code: {do_we_really}", 
                            title="On-Demand Run Failed ⚠️", 
                            style="danger", 
                            timeout=10).show()


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








