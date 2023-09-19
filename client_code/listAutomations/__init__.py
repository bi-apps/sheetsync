from ._anvil_designer import listAutomationsTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
import anvil.js
from .ItemTemplate5 import ItemTemplate5
 
class listAutomations(listAutomationsTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Hide Components -----
        # self.repeating_panel_1.width = "100%"


        # Get User Specific Data -----
        # Get logged in User Object or return to home if not logged in
        self.user = anvil.users.get_user()
        self.setup_screen_counters()
        # Populate automation groups dropdown
        self.populate_automation_groups()


    def populate_automation_groups(self):
        # Fetch all the automation records for this user
        all_automations = self.automations
    
        # Extract unique automation groups
        unique_groups = set()
        for automation in all_automations:
            automation_group = automation['automation_group']
            if automation_group:  # This checks if automation_group is not None or empty
                unique_groups.add(automation_group)
    
        # Convert the set to a list of tuples (this format is compatible with Anvil dropdown items)
        dropdown_items = [(group, group) for group in unique_groups]
    
        # Set these as the items for the dropdown
        self.filter_by_group_dropdown.items = dropdown_items

    def setup_screen_counters(self, **event_args):
        self.automations = app_tables.tb_automation_type_1_2.search(user=self.user)

        
        self.totalAutomationsLbl.text = self.user['automation_count']
        # Count the enabled automations
        count_enabled = sum(1 for automation in self.automations if automation['map_enabled'])
        print(count_enabled)
        self.activeAutomationsLbl.text = str(count_enabled)

        count_standard = sum(1 for automation in self.automations if automation['map_type']==1)
        self.standardAutomationsLbl.text = count_standard

        count_criteria = sum(1 for automation in self.automations if automation['map_type']==2)
        self.criteriaAutomationLbl.text = count_criteria



    # def data_row_panel_1_show(self, **event_args):
    #     """This method is called when the data row panel is shown on the screen"""
    #     tables.app_tables.tb_automation_type_1_2.search(user=self.user)

    def list_automations_repeating_panel_show(self, **event_args):
        """This method is called when the RepeatingPanel is shown on the screen"""
        # self.automation_list = tables.app_tables.tb_automation_type_1_2.search(user=self.user)
        self.list_automations_repeating_panel.items = self.automations


    def searchInputChange(self, **event_args):
        """This method is called when the text in this text box is edited"""
        search_string = self.searchInput.text.lower()
        self.list_automations_repeating_panel.items = []
        self.list_automations_repeating_panel.items = tables.app_tables.tb_automation_type_1_2.search(map_name=q.full_text_match(search_string))
        # items = tables.app_tables.tb_automation_type_1_2.search(map_name=q.ilike('%' + search_string + '%'))
        # items_list = list(items)  # Convert SearchIterator to list
        # # print("Items returned by query:", items_list)
        # self.list_automations_repeating_panel.items = []
        # self.list_automations_repeating_panel.items = items_list
        return



    def listHomeBtn_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('indexPage')

    def listBuildBtn_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('mapperHome')

    def listViewBtn_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('listAutomations')

    def listSettingsBtn_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('settings')

    def filter_by_group_dropdown_change(self, **event_args):
        """This method is called when an item is selected"""
        selected_group = self.filter_by_group_dropdown.selected_value
        if selected_group is not None:
            self.list_automations_repeating_panel.items = tables.app_tables.tb_automation_type_1_2.search(automation_group=q.ilike('%' + selected_group + '%'))
            return
        else:
            self.list_automations_repeating_panel.items = self.automations
            return



















