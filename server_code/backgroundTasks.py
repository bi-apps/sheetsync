import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime, timedelta
from .helperFunctions import should_execute, background_get_result_code_or_message
from .authenticationFunctions import get_smartsheet_client_object
from .sheetFunctions import get_column_data_without_criteria


""" Global Threshold Interval settings"""
task_run_interval = 5 # minutes
""" Change this with cuation """

# Return Al registered and enabled users
def find_clients(*args, **kwargs):
    print("Finding Clients")
    return app_tables.users.search(enabled=True, automation_count=q.greater_than(0))

def find_active_projects(*args, **kwargs):
    print("Finding Active projects")
    return app_tables.db_sd_one_to_one.search(user=kwargs['client'])

def can_i_do_this_project(*args, **kwargs):
    # Check If this project has never been executed
    project = kwargs['current_project']
    #
    if project['last_executed'] is None:
        return True
    else:
        print("Project was laste Executed at:")
        print(project['last_executed'])
        # Check if this task last execute date time has reached the task interval threshold, if True = execute, False = Skip
        if should_execute(project['last_executed'], task_run_interval):
            return True
        else:
            return False

def get_me_the_correct_cement(*args, **kwargs):
    if kwargs['destination_column_type'] not in ["CONTACT_LIST", "MULTI_CONTACT_LIST"]:
        new_column_obj = {
            "options": kwargs['new_destination_column_values'],
            "type": kwargs['destination_column_type'],
            "validation": kwargs['destination_column_validation']
        }
    else:
        # If the Destination Column type is a Contact Column Type build the Contact Dropdown Column Object
        # ---------------- Conect Column Type Specific Code ------------------------ #
        new_column_obj = {
            "contact_options": kwargs['new_destination_column_values'],
            "type": kwargs['destination_column_type'],
            "validation": kwargs['destination_column_validation']
        }
    return new_column_obj

def sign_project_off(*args, **kwargs):
    updated_destination_column = kwargs['client'].Sheets.update_column(
        sheet_id=kwargs['destination_sheet_id'],
        column_id=kwargs['destination_column_id'],
        column_obj=kwargs['new_column_obj']
        )
    # Return the call result
    return background_get_result_code_or_message(updated_destination_column)

def update_the_project_last_execution(*args, **kwargs):
    project_to_update = kwargs['project_details'].update(last_executed=datetime.now())
    return project_to_update

def log_project(*args, **kwargs):
    add_log = app_tables.job_logs.add_row(user=kwargs['client_details'],
                                          automation_name=kwargs['project_details']['map_name'],
                                          job_log_details=kwargs['log_details'],
                                          log_datatime=datetime.now())
    return add_log
    
def execute_no_criteria_project(*args, **kwargs):
    # Initiate a Smartsheet API Client Instance to use for the Specific Client
    smartsheet_api = get_smartsheet_client_object(kwargs['client_details'])
    # Get Project Details from Keyword Args
    project_details = kwargs['project_details']
    # Get New Column Values from Source Sheet
    new_column_values = get_column_data_without_criteria(smartsheet_api,
                                                         project_details['src_sheet_id'],
                                                         project_details['src_sheet_col_id'])
    # Get the destination sheet's column Options i.e Picklist, Contact column etc
    get_destination_column_options = smartsheet_api.Sheets.get_column(sheet_id=project_details['dest_sheet_id'],
                                                              column_id=project_details['dest_col_id'])
    # Get the correct Payload object for the API call from get_me_the_correct_cement function
    column_object = get_me_the_correct_cement(destination_column_type=project_details['dest_column_type'],
                                              destination_column_validation=project_details['dest_column_validation'],
                                              new_destination_column_values=new_column_values)
    # Call the comon component to send HTTP POST Request to smartsheets API
    project_signed_off = sign_project_off(client=smartsheet_api,
                                          destination_sheet_id=project_details['dest_sheet_id'],
                                          destination_column_id=project_details['dest_col_id'],
                                          new_column_obj=column_object)
    if project_signed_off == 0:
        print("sucess")
        project_updated = update_the_project_last_execution(project_details=project_details)
    else:
        print("failed")
        print(project_signed_off)
        write_project_log = log_project(client_details=kwargs['client_details'],
                                        project_details = project_details,
                                        log_details = project_signed_off)
        print("write_project_log")
        print(write_project_log)
    
    return project_signed_off


def get_contracts(*args, **kwargs):
    # Get all Active Clients
    active_clients = find_clients()
    
    # loop Trough all active Clients and get there Jobs to run
    for client in active_clients:
        # Get all Projects for the respective client
        project_list = find_active_projects(client=client)
        
        # loop Trough all active Projects and Validate there last executing datetime
        for project in project_list:
            # Check if can execute this project now
            execute_now = can_i_do_this_project(current_project=project)
            # If True = Execute Now
            if execute_now:
                print("executing now")
                client_details = client
                project_details = project
                c = execute_no_criteria_project(client_details=client, project_details=project)
                print(c)
                
            # If False = Skip
            else:
                print("Should not execute")
                print(execute_now)

    return




@anvil.server.background_task
def project_manager(*args, **kwargs):
    testJob = get_contracts()
    # print(testJob)
    # pass
