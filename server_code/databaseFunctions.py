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
             
             created_date_timestamp=datetime.now(),
             automation_group=kwargs.get('automation_group', None)
           )
           return True
         except tables.TableError as saveError:
           return str(saveError)

@anvil.server.callable
def save_automation(*args, **kwargs):
        try:
            kwargs['database'].add_row(
                user=kwargs.get('user_obj', None),
                
                map_enabled=kwargs.get('map_enabled', None),
                map_name=kwargs.get('map_name', None),
                map_type=kwargs.get('map_type', None),
                
                src_sheet_name=kwargs.get('source_sheet_name', None),
                src_sheet_id=kwargs.get('source_sheet_id', None),
                src_sheet_col_name=kwargs.get('source_col_name', None),
                src_sheet_col_id=kwargs.get('source_col_id', None),
                
                dest_sheet_name=kwargs.get('dest_sheet_name', None),
                dest_sheet_id=kwargs.get('dest_sheet_id', None),
                dest_sheet_col_name=kwargs.get('dest_col_name', None),
                dest_sheet_col_id=kwargs.get('dest_col_id', None),

                dest_sheet_col_type_name=kwargs.get('dest_col_type_name', None),
                dest_sheet_col_type=kwargs.get('dest_col_type', None),
                dest_sheet_col_validation=kwargs.get('dest_col_validation', None),
                
                criterion_type=kwargs.get('criterion_type', None),
                
                criterion_src_sheet_name=kwargs.get('criterion_source_sheet_name', None),
                criterion_src_sheet_id=kwargs.get('criterion_source_sheet_id', None),
                criterion_src_sheet_col_name=kwargs.get('criterion_source_sheet_col_name', None),
                criterion_src_sheet_col_id=kwargs.get('criterion_source_sheet_col_id', None),
                
                criterion_operator_type_name=kwargs.get('criterion_operator_name', None),
                criterion_operator_type_value=kwargs.get('criterion_operator_value', None),
                
                criterion_dest_sheet_name=kwargs.get('criterion_dest_sheet_name', None),
                criterion_dest_sheet_id=kwargs.get('criterion_dest_sheet_id', None),
                criterion_dest_sheet_col_name=kwargs.get('criterion_dest_sheet_col_name', None),
                criterion_dest_sheet_col_id=kwargs.get('criterion_dest_sheet_col_id', None),
                
                criterion_value=kwargs.get('criterion_values', None),
                
                created_date_timestamp=datetime.now(),

                last_executed=datetime.now(),

                automation_group=kwargs.get('automation_group', None)
            )
            
            # Increment user Automation Count On Sucessful Saving
            automation_count = kwargs['user_obj']['automation_count']
            automation_count += 1
            kwargs['user_obj'].update(automation_count=automation_count)
            # Return True When Done

            selected_group = kwargs.get('automation_group', None)
            if selected_group is not None:
                selected_group_count = app_tables.groups.get(user=kwargs['user_obj'], group=selected_group)
                group_count = selected_group_count['automation_count']
                group_count += 1
                selected_group_count.update(automation_count=group_count)
            
            return True
        except tables.TableError as saveError:
           return str(saveError)

@anvil.server.callable
def update_automation(row_id, *args, **kwargs):
    try:
        # Fetch the row you want to update from the database
        row_to_update = kwargs['database'].get_by_id(row_id)

        # Ensure that the row exists
        if not row_to_update:
            raise Exception(f"Row with ID {row_id} not found")

        # Update the row with the provided values
        row_to_update.update(
            user=kwargs.get('user_obj', None),
            map_enabled=kwargs.get('map_enabled', None),
            map_name=kwargs.get('map_name', None),
            map_type=kwargs.get('map_type', None),
            src_sheet_name=kwargs.get('source_sheet_name', None),
            src_sheet_id=kwargs.get('source_sheet_id', None),
            src_sheet_col_name=kwargs.get('source_col_name', None),
            src_sheet_col_id=kwargs.get('source_col_id', None),
            dest_sheet_name=kwargs.get('dest_sheet_name', None),
            dest_sheet_id=kwargs.get('dest_sheet_id', None),
            dest_sheet_col_name=kwargs.get('dest_col_name', None),
            dest_sheet_col_id=kwargs.get('dest_col_id', None),
            dest_sheet_col_type_name=kwargs.get('dest_col_type_name', None),
            dest_sheet_col_type=kwargs.get('dest_col_type', None),
            dest_sheet_col_validation=kwargs.get('dest_col_validation', None),
            criterion_type=kwargs.get('criterion_type', None),
            criterion_src_sheet_name=kwargs.get('criterion_source_sheet_name', None),
            criterion_src_sheet_id=kwargs.get('criterion_source_sheet_id', None),
            criterion_src_sheet_col_name=kwargs.get('criterion_source_sheet_col_name', None),
            criterion_src_sheet_col_id=kwargs.get('criterion_source_sheet_col_id', None),
            criterion_operator_type_name=kwargs.get('criterion_operator_name', None),
            criterion_operator_type_value=kwargs.get('criterion_operator_value', None),
            criterion_dest_sheet_name=kwargs.get('criterion_dest_sheet_name', None),
            criterion_dest_sheet_id=kwargs.get('criterion_dest_sheet_id', None),
            criterion_dest_sheet_col_name=kwargs.get('criterion_dest_sheet_col_name', None),
            criterion_dest_sheet_col_id=kwargs.get('criterion_dest_sheet_col_id', None),
            criterion_value=kwargs.get('criterion_values', None),
            last_executed=datetime.now(),
            automation_group=kwargs.get('automation_group', None)
        )
        return True
    except Exception as e:
        # Handle the exception (e.g., log it, re-raise it, etc.)
        return str(e)
        
@anvil.server.callable
def delete_automation(*args, **kwargs):
    row_to_delete = app_tables.tb_automation_type_1_2.get_by_id(kwargs['row_id'])
    automation_count = kwargs['user']['automation_count']
    if not row_to_delete:
        raise Exception(f"Row with ID {kwargs['row_id']} not found")

    print(row_to_delete.delete())
    automation_count -= 1
    kwargs['user'].update(automation_count=automation_count)
    
    return True