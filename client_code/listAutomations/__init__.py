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

class listAutomations(listAutomationsTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Hide Components -----


        # Get User Specific Data -----
        # Get logged in User Object or return to home if not logged in
        self.user = anvil.users.get_user()
        # if not user:
        #   open_form('homePage')

    def flow_panel_2_show(self, **event_args):
        """This method is called when the FlowPanel is shown on the screen"""
        self.repeatingPanelMain.items = tables.app_tables.tb_automation_type_1_2.search(user=self.user)

    def addMappingButton_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('mapperHome')

    def data_row_panel_1_show(self, **event_args):
        """This method is called when the data row panel is shown on the screen"""
        tables.app_tables.tb_automation_type_1_2.search(user=self.user)



