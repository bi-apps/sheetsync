from ._anvil_designer import homePageTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users



class homePage(homePageTemplate):
  def __init__(self, **properties):

    # Set Form properties and Data Bindings.

    self.init_components(**properties)



    # Any code you write here will run before the form opens.

  def primary_color_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.login_with_form()

  def primary_color_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.signup_with_form()


