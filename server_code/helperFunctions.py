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


# Helper Function to Get the result code if Sucessfull or return the error message if error
def get_result_code_or_message(updated_destination_column):
    if isinstance(updated_destination_column, smartsheet.models.Error):
        return updated_destination_column.result.message
    else:
        return updated_destination_column.result_code

# Helper function to convert response values to contact dictionaries
def create_contact(email):
    return {"email": email, "name": email}

# Helper Function To Check that Automation Name is unique
@anvil.server.callable
def is_mapping_name_unique(user, mapping_name, mapping_table):
    # Check if there is any existing row with the same mapping name for the user
    existing_mappings = mapping_table.search(user=user, map_name=mapping_name)
    if len(existing_mappings) == 0:
      return True
    else:
      return False




