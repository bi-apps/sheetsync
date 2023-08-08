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
    client = getSmartsheetClient(kwargs['userId'])

    testingCriteriaColumValues = getColumnDataWithCriteria(kwargs['userId'],
                                                           kwargs['selectedSourceSheetId'],
                                                           kwargs['selectedSourceSheetColumnId'],
                                                           kwargs['selectedOneToOneCriterionSourceColumnId'],
                                                           kwargs['selectedOntToOneCriterionValue'],
                                                           kwargs['selectedOntToOneCriterionValue'],
                                                           )
    print(testingCriteriaColumValues)
