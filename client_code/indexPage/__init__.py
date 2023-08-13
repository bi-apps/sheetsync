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
  def __init__(self, user=None ,**properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Hide Components -----
    # Hide Connect Smartsheet Button on Load
    self.connectSmartsheetBtn.visible = False
    # Hide total sheet count on load 
    self.totalSheetsColum.visible = False
    
    # Get User Specific Data -----
    # Get logged in User Object or return to home if not logged in
    if user is None:
        self.user = anvil.users.get_user()
    else:
        self.user = user
    # if not user:
    #   open_form('homePage')
    
    # Set Heading to User Name / Email
    self.headLine.text = f"Welcome {self.user['email']}"

    # Start Logic -----
    # Get Smartsheet's Auth Status
    authStatus = self.user['authenticated_to_smartsheets']
    if authStatus:
        try:
            # Get Sheet Info
            get_sheets_info = anvil.server.call('getSheetsInfo', self.user)
            
            # Ensure we have the data before proceeding
            if get_sheets_info is not None:
                # Update the sheet count
                self.totCountSheets.text = str(get_sheets_info['total_count'])
                
                # Update the operational data
                self.all_sheets = get_sheets_info['sheets']
                self.dataGridRepeatingPanelMain.items = self.all_sheets
    
        except Exception as e:
        # Handle any errors here, e.g., show an alert to the user
            print(f"Error fetching sheet info: {e}")
        
        # Enable Visual Effects
        self.connectSmartsheetBtn.visible = True
        self.connectSmartsheetBtn.remove_event_handler('click')
        self.connectSmartsheetBtn.text = 'Connected'
        self.connectSmartsheetBtn.icon = 'fa:check'
        self.connectSmartsheetBtn.background = '#4CAF50'
        self.totalSheetsColum.visible = True
    else:
        self.connectSmartsheetBtn.visible = True
        self.connectSmartsheetBtn.text = 'Connect To Smartsheets...'
        self.connectSmartsheetBtn.icon = 'fa:link'
        self.connectSmartsheetBtn.background = '#212121'
      
  # Start Smartsheets OAuth Flow.
  def connectSmartsheetBtn_click(self, **event_args):
    """This method is called when the button is clicked"""
    # user = anvil.users.get_user()
    auth_url = anvil.server.call('get_auth_url',self.user)
    anvil.js.window.open(auth_url, '_blank')
    return

  def searchInputChange(self, **event_args):
    """This method is called when the text in this text box is edited"""
    search_string = self.searchInput.text.lower()
    if len(search_string) > 5:
        if len(self.all_sheets) < 200:
            # Local search for smaller datasets
            filtered_sheets = [sheet for sheet in self.all_sheets if search_string in sheet['sheet_name'].lower()]
        else:
            # Server search for larger datasets
            filtered_sheets = anvil.server.call('searchSheets', self.user, search_string)
        
        # Update the RepeatingPanel's items
        self.dataGridRepeatingPanelMain.items = filtered_sheets

  def sign_out_user_on_click(self, **event_args):
    """This method is called when the link is clicked"""
    anvil.users.logout()
    open_form('homePage')
    return


  def indexHomeBtn_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('indexPage')

  def indexBuildBrn_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('mapperHome')

  def indexViewBtn_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('listAutomations')

  def indexSettingsBtn_click(self, **event_args):
      """This method is called when the button is clicked"""
      pass












    



    


      
    










