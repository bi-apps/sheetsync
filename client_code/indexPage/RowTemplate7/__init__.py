from ._anvil_designer import RowTemplate7Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate7(RowTemplate7Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def setupAutomationBtn_click(self, **event_args):
      """This method is called when the button is clicked"""
      print("Button Clicked on Repeating Panel")
      print(f"Row Data : {self.setupAutomationBtn.tag}")
      print(f"Sheet Name : {self.setupAutomationBtn.tag['sheet_name']}")
      print(f"Sheet Name : {self.setupAutomationBtn.tag['sheet_id']}")
      # self.raise_event('x-setup-clicked', row_data=self.setupAutomationBtn.tag)
      open_form('mapperHome', setup_data=self.setupAutomationBtn.tag)

