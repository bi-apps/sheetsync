from ._anvil_designer import indexPageTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class indexPage(indexPageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    anvil.users.logout()

  def form_show(self, **event_args):
    """This method is called when the HTML panel is shown on the screen"""
    smartsheetObj = anvil.server.call('smartApi')
    # response = smartsheetObj.Sheets.list_sheets()
    alert(smartsheetObj)
    


