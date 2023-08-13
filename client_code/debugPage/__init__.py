from ._anvil_designer import debugPageTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class debugPage(debugPageTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        anvil.users.login_with_form()
        self.user = anvil.users.get_user()
        print(self.user)
        # Any code you write here will run before the form opens.

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        # response = get_sheets_info = anvil.server.call('getSheetsInfo', self.user)
        response = anvil.server.call("get_smartsheet_client_object", self.user)
        print(response)

