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
    
    # self.dataGridRepeatingPanelMain.items = tables.app_tables.sheets.search()
    
    self.connectSmartsheetBtn.visible = False

    # Do not display total sheet section when loading
    self.totalSheetsColum.visible = False
    
    # remeber to get user details and add below dynamically!
    self.headLine.text = 'Welcome User'

    authStatus = anvil.server.call('check_auth_status','userId')
    if authStatus:
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
      
    try:
      self.totCountSheets.text = tables.app_tables.auth_data.get(user='userId')['totalSheetsInAccount']
    except:
      pass
    

  def connectSmartsheetBtn_click(self, **event_args):
    """This method is called when the button is clicked"""
    auth_url = anvil.server.call('get_auth_url')
    anvil.js.window.open(auth_url, '_blank')

  def form_show(self, **event_args):
    """This method is called when the HTML panel is shown on the screen"""
    


  def dataGridMain_show(self, **event_args):
    """This method is called when the data grid is shown on the screen"""
    self.dataGridRepeatingPanelMain.items = tables.app_tables.sheets.search()


  def searchInputChange(self, **event_args):
    """This method is called when the text in this text box is edited"""
    allItems = self.dataGridRepeatingPanelMain.items
    search_string = self.searchInput.text.lower()
    
    if len(search_string) > 2:
        filtered_items = [item for item in self.dataGridRepeatingPanelMain.items if search_string in item['sheet_name'].lower()]
        self.dataGridRepeatingPanelMain.items = filtered_items
    else:
        filtered_items = allItems
        self.dataGridRepeatingPanelMain.items = filtered_items


    


      
    










