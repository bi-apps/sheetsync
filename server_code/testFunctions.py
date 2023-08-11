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
from .helperFunctions import get_result_code_or_message

@anvil.server.callable
def houstonWeHaveAProblem(*args, **kwargs):
    client = getSmartsheetClient(kwargs['user_id'])
    #
    get_criteria_based_filtered_column_values = getColumnDataWithCriteria(kwargs['user_id'],
                                                          kwargs['selected_source_sheet_id'],
                                                          kwargs['selected_source_sheet_column_id'],
                                                          kwargs['selected_criteria_source_column_id'],
                                                          kwargs['selected_criteria_value'],
                                                          kwargs['selected_criteria_operator'])
     # If the Destination Selected Column Type is not Contact column types Continue as normal dropdowns
    
    if kwargs['selected_destination_column_type_value'] not in ["CONTACT_LIST", "MULTI_CONTACT_LIST"]:
        new_column_obj = {
            "options": get_criteria_based_filtered_column_values,
            "type": kwargs['selected_destination_column_type_value'],
            "validation": kwargs['selected_destination_column_validation']
        }
    else:
        # If the Destination Column type is a Contact Column Type build the Contact Dropdown Column Object
        # ---------------- Conect Column Type Specific Code ------------------------ #
        new_column_obj = {
            "contact_options": get_criteria_based_filtered_column_values,
            "type": kwargs['selected_destination_column_type_value'],
            "validation": kwargs['selected_destination_column_validation']
        }
     # Update the Destination Sheet with the New Destination Column Values
    updated_destination_column = client.Sheets.update_column(
        sheet_id=kwargs['selected_destination_sheet_id'],
        column_id=kwargs['selected_destination_sheet_column_id'],
        column_obj=new_column_obj
     )
     # Return the call result
    return get_result_code_or_message(updated_destination_column)
     # return get_criteria_based_filtered_column_values
