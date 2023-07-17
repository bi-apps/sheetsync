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

  def signIn_user_click_event(self, **event_args):
    """This method is called when the button is clicked"""
    user = anvil.users.get_user()
    if user:
      open_form('indexPage')
    else:
      anvil.users.login_with_form(show_signup_option=False, allow_cancel=True, remember_by_default=True)
    return

  def signup_user_click_event(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.signup_with_form(allow_cancel=True)
    return






