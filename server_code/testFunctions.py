import anvil.stripe
import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import smartsheet
from .sheetFunctions import getSmartsheetClient, getColumnDataWithCriteria

@anvil.server.callable
def houstonWeHaveAProblem(*args, **kwargs):
    client = getSmartsheetClient(kwargs['user_id'])

    testingCriteriaColumValues = getColumnDataWithCriteria(kwargs['user_id'],
                                                          kwargs['selected_source_sheet_id'],
                                                          kwargs['selected_source_sheet_column_id'],
                                                          kwargs['selected_criteria_source_column_id'],
                                                          kwargs['selected_criteria_value'],
                                                          kwargs['selected_criteria_operator'])
    print(testingCriteriaColumValues)
