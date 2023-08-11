import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime

# Legend! Read this before Looking at the code please.....
############# Maping types #########################################
# One To One Mapping = 1 (kwargs['map_type'] == 1)
# Criteria Based One To One Mapping = 2 (kwargs['map_type'] == 2)
#
#
####################################################################

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

    if kwargs['map_type'] == 2:
         try:
           kwargs['database'].add_row(
             
             user=kwargs['user'],

             map_enabled=kwargs['map_enabled'],
             map_name=kwargs['map_name'],
             
             src_sheet_name=kwargs['source_sheet_name'],
             src_sheet_id=kwargs['source_sheet_id'],
             src_sheet_col_name=kwargs['source_col_name'],
             src_sheet_col_id=kwargs['source_col_id'],
             
             dest_sheet_name=kwargs['dest_sheet_name'],
             dest_sheet_id=kwargs['dest_sheet_id'],
             dest_sheet_col_name=kwargs['dest_col_name'],
             dest_sheet_col_id=kwargs['dest_col_id'],
             dest_sheet_col_type=kwargs['dest_col_type'],
             dest_sheet_col_validation=kwargs['dest_col_validation'],

             criterion_type=kwargs['criterion_type'],

             criterion_src_sheet_name=kwargs['criterion_source_sheet_name'],
             criterion_src_sheet_id=kwargs['criterion_source_sheet_id'],
             criterion_src_sheet_col_name=kwargs['criterion_source_sheet_col_name'],
             criterion_src_sheet_col_id=kwargs['criterion_source_sheet_col_id'],
               
             criterion_operator_type_name=kwargs['criterion_operator_name'],
             criterion_operator_type_value=kwargs['criterion_operator_value'],

             criterion_dest_sheet_name=kwargs['criterion_dest_sheet_name'],
             criterion_dest_sheet_id=kwargs['criterion_dest_sheet_id'],
             criterion_dest_sheet_col_name=kwargs['criterion_dest_sheet_col_name'],
             criterion_dest_sheet_col_id=kwargs['criterion_dest_sheet_col_id'],

             criterion_value=kwargs['criterion_values'],
             
             created_date_timestamp=datetime.now()
           )
           return True
         except tables.TableError as saveError:
           return str(saveError)
