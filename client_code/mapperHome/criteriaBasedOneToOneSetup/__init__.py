from ._anvil_designer import criteriaBasedOneToOneSetupTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class criteriaBasedOneToOneSetup(criteriaBasedOneToOneSetupTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    # Get User
    user = anvil.users.get_user()
    # Any code you write here will run before the form opens.
    sheet_data = anvil.server.call('getSheetData', user)
    self.oneToOneCriteriaBasedSourceSheetDropDown.items = [sheet['sheet_name'] for sheet in sheet_data]