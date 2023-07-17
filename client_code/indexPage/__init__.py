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

    # Hide Connect Smartsheet Button on Load
    self.connectSmartsheetBtn.visible = False

    # Do not display total sheet section when loading
    self.totalSheetsColum.visible = False

    # Get logged in User ID
    user = anvil.users.get_user()
    # remeber to get user details and add below dynamically!
    self.headLine.text = f'Welcome {user}'

    authStatus = anvil.server.call('check_auth_status',user)
    if authStatus:
      self.connectSmartsheetBtn.visible = True
      self.connectSmartsheetBtn.remove_event_handler('click')
      self.connectSmartsheetBtn.text = 'Connected'
      self.connectSmartsheetBtn.icon = 'fa:check'
      self.connectSmartsheetBtn.background = '#4CAF50'
      self.totalSheetsColum.visible = True
      # try:
        # self.totCountSheets.text = tables.app_tables.auth_data.get(user=user)['totalSheetsInAccount']
      self.totCountSheets.text = user['totalSheetsInAccount']
      # except:
        # pass
    else:
      self.connectSmartsheetBtn.visible = True
      self.connectSmartsheetBtn.text = 'Connect To Smartsheets...'
      self.connectSmartsheetBtn.icon = 'fa:link'
      self.connectSmartsheetBtn.background = '#212121'
      

  def connectSmartsheetBtn_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = anvil.users.get_user()
    auth_url = anvil.server.call('get_auth_url',user)
    anvil.js.window.open(auth_url, '_blank')

  def form_show(self, **event_args):
    """This method is called when the HTML panel is shown on the screen"""
    

  # def dataGridMain_show(self, **event_args):
  #   """This method is called when the data grid is shown on the screen"""
  #   user = anvil.users.get_user()
  #   self.dataGridRepeatingPanelMain.items = tables.app_tables.sheets.search(user=user)


  # def searchInputChange(self, **event_args):
  #     """This method is called when the text in this text box is edited"""
  #     search_string = self.searchInput.text.lower()
  #     self.dataGridRepeatingPanelMain.items = tables.app_tables.sheets.search(sheet_name=q.ilike('%' + search_string + '%'))


    


      
    










