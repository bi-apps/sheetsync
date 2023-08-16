from ._anvil_designer import settingsTemplate
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

class settings(settingsTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Get Logged in User
        self.user = anvil.users.get_user()
        # anvil.users.configure_account_with_form()
        self.groupsRepeatingPanel.items = app_tables.groups.search(user=self.user)

    def sign_out_user_on_click(self, **event_args):
        """This method is called when the link is clicked"""
        anvil.users.logout()
        open_form('homePage')

    def mapperHomeBtn_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('indexPage')

    def mapperBuildBtn_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('mapperHome')

    def mapperViewBtn_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('listAutomations')

    def mapperSettingsBtn_click(self, **event_args):
        """This method is called when the button is clicked"""
        pass

    def addGroupBtn_click(self, **event_args):
        """This method is called when the button is clicked"""
        add_group = self.group_names_txt.text
        if add_group:
            added_group = app_tables.groups.add_row(user=self.user,
                                                   group=add_group,
                                                   automation_count=0)
            print(added_group)
            if added_group:
                Notification("Group Added!",
                            title="Success",
                            style="success",
                            timeout=2).show()
            self.groupsRepeatingPanel.items = app_tables.groups.search(user=self.user)
            self.group_names_txt.text = ""
        else:
            Notification("No Group Name Specified!",
            title="Oops..",
            style="warning ",
            timeout=2).show()
            