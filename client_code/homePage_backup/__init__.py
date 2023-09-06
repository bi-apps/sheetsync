from ._anvil_designer import homePage_backupTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users



class homePage_backup(homePage_backupTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    # Delay the check using a timer
    is_logged_in = anvil.server.call('check_logged_in')
    if is_logged_in:
        open_form('indexPage', user=anvil.users.get_user())


    # # If a user is already logged in, open the index page
    # logged_in_user = anvil.users.get_user()
    # if logged_in_user:
    #    open_form('indexPage', user=logged_in_user)

  def signIn_user_click_event(self, **event_args):
      """This method is called when the button is clicked"""
      try:
         anvil.users.login_with_form(show_signup_option=False, allow_cancel=True, remember_by_default=True)
         # Directly open the index page after login
         open_form('indexPage')
      except anvil.users.AuthenticationFailed:
         # If login fails, just return and stay on the home page
         return


    # If login succeeds, open the index page
    # logged_in_user = anvil.users.get_user()
    # open_form('indexPage', user=logged_in_user)

  def signup_user_click_event(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.signup_with_form(allow_cancel=True)
    # After signup, check if a user is logged in
    logged_in_user = anvil.users.get_user()
    if logged_in_user:
      # If a user is logged in, open the index page
      open_form('indexPage', user=logged_in_user)






