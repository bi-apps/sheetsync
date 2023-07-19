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
from .oneToOneSetup import oneToOneSetupTemplate

class mapperHome(mapperHomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Get Logged in User
    user = anvil.users.get_user()
    # Source Sheet DropDown Selection
    # sheet_data = anvil.server.call('getSheetData', user)
    # self.sourceSheetDropDown.items = [sheet['sheet_name'] for sheet in sheet_data]
    

    # self.flow_panel_2.add_component(RelationshipMappingForm())
  def sign_out_user_on_click(self, **event_args):
    """This method is called when the link is clicked"""
    anvil.users.logout()
    open_form('homePage')

  # class RelationshipMappingForm(Form):
  #     def __init__(self, **properties):
  #         super().__init__(**properties)
  #         self.source_sheet_dropdown = DropDown()
  #         self.destination_mappings = []
  #         self.add_destination_button = Button(text="Add Destination", role="secondary")
          
  #         self.add_component(self.source_sheet_dropdown)
  #         self.add_component(self.add_destination_button)
          
  #         self.add_destination_button.set_event_handler('click', self.add_destination)
          
  #     def add_destination(self, **event_args):
  #         destination_sheet_dropdown = DropDown()
  #         destination_column_dropdown = DropDown()
  #         remove_destination_button = Button(text="Remove", role="secondary")
          
  #         destination_mapping = {'sheet_dropdown': destination_sheet_dropdown, 'column_dropdown': destination_column_dropdown, 'remove_button': remove_destination_button}
  #         self.destination_mappings.append(destination_mapping)
          
  #         destination_section = ColumnPanel()
  #         destination_section.add_component(destination_sheet_dropdown)
  #         destination_section.add_component(destination_column_dropdown)
  #         destination_section.add_component(remove_destination_button)
          
  #         self.add_component(destination_section)
          
  #         remove_destination_button.set_event_handler('click', self.remove_destination, destination_mapping)
          
  #     def remove_destination(self, **event_args):
  #         destination_mapping = event_args['sender']
  #         self.destination_mappings.remove(destination_mapping)
  #         destination_mapping.remove_from_parent()

  def oneToOneBtnSelected(self, **event_args):
    """This method is called when the button is clicked"""
    self.mainGridPanelMappings.visible = False
    self.mainPageColumn.clear()
    self.mainPageColumn.add_component(oneToOneSetupTemplate())
    

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








