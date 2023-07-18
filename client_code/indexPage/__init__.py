from ._anvil_designer import indexPageTemplate
from anvil import *
import plotly.graph_objects as go
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
    # Hide Components -----
    # Hide Connect Smartsheet Button on Load
    self.connectSmartsheetBtn.visible = False
    # Hide total sheet count on load 
    self.totalSheetsColum.visible = False
    
    # Get User Specific Data -----
    # Get logged in User Object or return to home if not logged in
    user = anvil.users.get_user()
    if not user:
      open_form('homePage')
    
    # Set Heading to User Name / Email
    self.headLine.text = f"Welcome {user['email']}"

    # Start Logic -----
    # Get Smartsheet's Auth Status
    authStatus = anvil.server.call('check_auth_status',user)
    if authStatus:
      # Get Sheet Counts
      if anvil.server.call('getSheetsCount',user):
        self.totCountSheets.text = user['totalSheetsInAccount']
        
      # Get Sheet Data
      self.dataGridRepeatingPanelMain.items = anvil.server.call('getSheetData')
        
      # Enable Visual Effects
      self.connectSmartsheetBtn.visible = True
      self.connectSmartsheetBtn.remove_event_handler('click')
      self.connectSmartsheetBtn.text = 'Connected'
      self.connectSmartsheetBtn.icon = 'fa:check'
      self.connectSmartsheetBtn.background = '#4CAF50'
      self.totalSheetsColum.visible = True
      # try:
        # self.totCountSheets.text = tables.app_tables.auth_data.get(user=user)['totalSheetsInAccount']
      
      # except:
        # pass
    else:
      self.connectSmartsheetBtn.visible = True
      self.connectSmartsheetBtn.text = 'Connect To Smartsheets...'
      self.connectSmartsheetBtn.icon = 'fa:link'
      self.connectSmartsheetBtn.background = '#212121'
      
  # Start Smartsheets OAuth Flow.
  def connectSmartsheetBtn_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = anvil.users.get_user()
    auth_url = anvil.server.call('get_auth_url',user)
    anvil.js.window.open(auth_url, '_blank')

  
  def form_show(self, **event_args):
    """This method is called when the HTML panel is shown on the screen"""



  def searchInputChange(self, **event_args):
      """This method is called when the text in this text box is edited"""
      search_string = self.searchInput.text.lower()
      self.dataGridRepeatingPanelMain.items = tables.app_tables.sheets.search(sheet_name=q.ilike('%' + search_string + '%'))

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    anvil.users.logout()



    


      
    










