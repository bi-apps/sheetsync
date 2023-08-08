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

# Helper Function To Save Automation for One To One Mapping ONLY
@anvil.server.callable
def saveMapping(*args, **kwargs):
    # Try Saving the data to the Database based on the Mapping Type
    if kwargs['map_type'] == 1:
         try:
           kwargs['database'].add_row(
             
             user=kwargs['user_obj'],

             map_enabled=kwargs['map_enabled'],
             map_name=kwargs['map_name'],
             
             src_sheet_name=kwargs['source_sheet_name'],
             src_sheet_id=kwargs['source_sheet_id'],
             src_sheet_col_name=kwargs['source_column_name'],
             src_sheet_col_id=kwargs['source_colum_id'],
             
             dest_sheet_name=kwargs['destination_sheet_name'],
             dest_sheet_id=kwargs['destination_sheet_id'],
             dest_col_name=kwargs['destination_column_name'],
             dest_col_id=kwargs['destination_colum_id'],
             dest_column_type=kwargs['destination_colum_type'],
             dest_column_validation=kwargs['destination_column_validation'],

             created_DateStamp=datetime.now()
           )
           return True
         except tables.TableError as saveError:
           return str(saveError)
