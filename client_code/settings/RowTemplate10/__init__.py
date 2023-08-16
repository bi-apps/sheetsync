from ._anvil_designer import RowTemplate10Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate10(RowTemplate10Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    def deleteGroupBtn_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.group = self.deleteGroupBtn.tag
        if self.group['automation_count'] > 0:
            confirm_from_user = confirm(f"You are about to delete a Group that's associated to {self.group['automation_count']} automations, This will ungroup these automations",
                                        large=True,
                                        dismissible=False,
                                        title="Are you sure?",)
            if confirm_from_user:
                self.deleted_group = app_tables.groups.get_by_id(self.group.get_id()).delete()
                print(self.deleted_group)
                Notification("Group Deleted!",
                            title="Delete Group",
                            style="info",
                            timeout=2).show()
                open_form('settings')
            else:
                return
        else:
            self.deleted_group = app_tables.groups.get_by_id(self.group.get_id()).delete()
            print(self.deleted_group)
            Notification("Group Deleted!",
                        title="Delete Group",
                        style="info",
                        timeout=2).show()
            open_form('settings')
        


