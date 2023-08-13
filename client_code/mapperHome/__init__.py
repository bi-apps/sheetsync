from ._anvil_designer import mapperHomeTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
import anvil.js
from .oneToOneSetup import oneToOneSetup

class mapperHome(mapperHomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Get Logged in User
    self.user = anvil.users.get_user()

  def sign_out_user_on_click(self, **event_args):
    """This method is called when the link is clicked"""
    anvil.users.logout()
    open_form('homePage')


  def oneToOneBtnSelected(self, **event_args):
    """This method is called when the button is clicked"""
    self.mainGridPanelMappings.visible = False
    self.mainPageColumn.clear()

    # Create an instance of the oneToOneSetup form and pass the user variable
    one_to_one_setup_form = oneToOneSetup(user=self.user)

    # Add the oneToOneSetup form as a subform to the mainPageColumn
    self.mainPageColumn.add_component(one_to_one_setup_form)

    # Show the oneToOneSetup form
    one_to_one_setup_form.visible = True
    

  def oneToManyBtnClick(self, **event_args):
    """This method is called when the button is clicked"""
    self.mainGridPanelMappings.visible = False

  def manyToOneBtnClick(self, **event_args):
    """This method is called when the button is clicked"""
    self.mainGridPanelMappings.visible = False

  def criteriaBasedOneToOneClick(self, **event_args):
    """This method is called when the button is clicked"""
    self.mainGridPanelMappings.visible = False

  def criteriaBasedOneToManyBtnClick(self, **event_args):
    """This method is called when the button is clicked"""
    self.mainGridPanelMappings.visible = False

  def criteriaBasedManyToOneBtnClick(self, **event_args):
    """This method is called when the button is clicked"""
    self.mainGridPanelMappings.visible = False

  def mapperHomeBtn_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('indexPage')

  def mapperBuildBtn_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('mapperHome')

  def mapperViewBtn_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('listAutomations')

  def mapperSettingsBtn_click(self, **event_args):
      """This method is called when the button is clicked"""
      pass












