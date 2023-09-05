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


    def setup_screen_counters(self, **event_args):
        automations = app_tables.tb_automation_type_1_2.search(user=self.user)

        
        self.totalAutomationsLbl.text = self.user['automation_count']
        # Count the enabled automations
        count_enabled = sum(1 for automation in automations if automation['map_enabled'])
        print(count_enabled)
        self.activeAutomationsLbl.text = str(count_enabled)

        count_standard = sum(1 for automation in automations if automation['map_type']==1)
        self.standardAutomationsLbl.text = count_standard

        count_criteria = sum(1 for automation in automations if automation['map_type']==2)
        self.criteriaAutomationLbl.text = count_criteria



    # def data_row_panel_1_show(self, **event_args):
    #     """This method is called when the data row panel is shown on the screen"""
    #     tables.app_tables.tb_automation_type_1_2.search(user=self.user)

    def list_automations_repeating_panel_show(self, **event_args):
        """This method is called when the RepeatingPanel is shown on the screen"""
        self.list_automations_repeating_panel.items = tables.app_tables.tb_automation_type_1_2.search(user=self.user)


    def searchInputChange(self, **event_args):
        """This method is called when the text in this text box is edited"""
        search_string = self.searchInput.text.lower()
        self.list_automations_repeating_panel.items = tables.app_tables.tb_automation_type_1_2.search(map_name=q.ilike('%' + search_string + '%'))
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
        pass


















