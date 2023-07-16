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

    # Any code you write here will run before the form opens.

  
  def form_show(self, **event_args):
    """This method is called when the HTML panel is shown on the screen"""
    # self.totCheetCount.text = anvil.server.call('getSheets')
    # Use the function
    def check_auth_status():
      # Get the current URL hash
      url_hash = anvil.get_url_hash()
      
      # Split the hash into components based on '?'
      components = url_hash.split('?')
      
      # If there are no query parameters, return None
      if len(components) < 2:
          return None
      
      # Split the query parameters based on '&'
      parameters = components[1].split('&')
      
      # Process each parameter
      for parameter in parameters:
          # Split the parameter into a key and a value
          key, value = parameter.split('=')
          
          # If the key is 'authenticated', return the value
          if key == 'authenticated':
              return value
      
      # If 'authenticated' is not a parameter, return None
      return None

    
    auth_status = check_auth_status()
    if auth_status == 'True':
        self.authText.content = auth_status
        print('Authenticated!')
    elif auth_status == 'false':
        self.authText.content = auth_status
        print('Authentication failed.')
    else:
        self.authText.content =" None"
        print('No authentication status.')

  def primary_color_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def connectSmartsheetBtn_click(self, **event_args):
    """This method is called when the button is clicked"""
    auth_url = anvil.server.call('get_auth_url')
    anvil.js.window.open(auth_url, '_blank')









