from ._anvil_designer import indexPageTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
import anvil.js

class indexPage(indexPageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def connectSmartsheetBtn_click(self, **event_args):
    """This method is called when the button is clicked"""
    auth_url = anvil.server.call('get_auth_url')
    anvil.js.window.open(auth_url, '_blank')

  def form_show(self, **event_args):
    """This method is called when the HTML panel is shown on the screen"""
    # Get the current URL hash
    url_hash = anvil.get_url_hash()
    
    # Split the hash into components based on '?'
    components = url_hash.split('?')
    self.authText.text = components
    return










