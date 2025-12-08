import sqlite3
import streamlit as st
import pandas as pd
from db_path import DB_PATH
from datetime import datetime
from time import sleep

# Initialize session state variables
if 'data_version' not in st.session_state:
    st.session_state['data_version'] = 0

# This flag is used to show a success message after an update
if 'success_update_message' not in st.session_state:
    st.session_state['success_update_message'] = False

# Store the count of updated tasks for the success message
if 'updated_tasks_count' not in st.session_state:
    st.session_state['updated_tasks_count'] = 0

# Initialize a list in session state to store debug messages
if 'debug_messages' not in st.session_state:
    st.session_state['debug_messages'] = []

@st.cache_data
def load_tasks(data_version):
    """
    Loads tasks from the database.
    The data_version argument is used to invalidate the cache
    when tasks are added, updated, or deleted.
    """
    conn = sqlite3.connect(DB_PATH, timeout=10)
    try:
        df = pd.read_sql_query('SELECT * FROM tasks ORDER BY created_date DESC', conn)

        df['completed'] = df['completed'].astype(bool)

        # Ensure completed_date is datetime or None for proper display/editing
        # 'coerce' will turn invalid date strings (like NULL from DB) into NaT (Not a Time)
        df['created_date'] = pd.to_datetime(df['created_date'],
                                            errors = 'coerce')
        df['completed_date'] = pd.to_datetime(df['completed_date'],
                                              errors='coerce')
        return df
    finally:
        conn.close()

def update_task_in_db(task_id, task_description, completed_status, completed_date):
    """
    Updates a single task in the database.
    completed_date should be a datetime object or None.
    """
    st.session_state['debug_messages'].append(f"{datetime.now().strftime('%H:%M:%S')} - DEBUG: update_task_in_db called for task_id: {task_id}")
    st.session_state['debug_messages'].append(f"{datetime.now().strftime('%H:%M:%S')} - DEBUG:   task_description: '{task_description}', completed_status: {completed_status}, completed_date: {completed_date}")
    conn = sqlite3.connect(DB_PATH, timeout=10)
    # Ensure task_id is an integer for the WHERE clause, handling potential NaN from pandas
    task_id_int = int(task_id) if not pd.isna(task_id) else None
    st.session_state['debug_messages'].append(f"{datetime.now().strftime('%H:%M:%S')} - DEBUG:   Original task_id type: {type(task_id)}, Converted task_id_int type: {type(task_id_int)}")


    cursor = conn.cursor()
    try:
        # Convert boolean to integer for SQLite
        completed_int = 1 if completed_status else 0
        
        # Convert datetime to string for SQLite, or None if it's NaT or None
        # Ensure completed_date is handled correctly if it's NaT from pandas
        completed_date_str = None
        if not pd.isna(completed_date): # Check if it's a valid datetime (not NaT)
            completed_date_str = completed_date.strftime('%Y-%m-%d %H:%M:%S')

        update_query = '''
        UPDATE tasks
        SET task = ?, completed = ?, completed_date = ?
        WHERE task_id = ?
        '''
        if task_id_int is None:
            print(f"ERROR: Cannot update task: task_id is invalid (None or NaN).")
            return False

        print(f"DEBUG:   Executing query: {update_query} with params: ('{task_description}', {completed_int}, '{completed_date_str}', {task_id_int})")
        print(f"DEBUG:   Type of task_id_int: {type(task_id_int)}")
        cursor.execute(update_query, (task_description, completed_int, completed_date_str, task_id_int))
        print(f"DEBUG:   Rows affected by update: {cursor.rowcount}")
        conn.commit()
        print(f"DEBUG:   Commit successful for task_id: {task_id}")
        return True # Indicate success
    
    except Exception as e:
        print(f"ERROR: Error updating task {task_id}: {e}") # Print to console for debugging
        st.error(f"Error updating task {task_id}: {e}")
        return False # Indicate failure
    
    finally:
        conn.close()

st.write(f'Run number: {st.session_state.data_version}')
st.header("📝 Update Your Tasks")

# Load tasks
try:
    df = load_tasks(st.session_state.data_version)
    
except Exception as e:
    st.error(f"Error loading tasks: {e}")
    df = pd.DataFrame() # Use an empty DataFrame on error

if not df.empty:
    # Define column configuration for st.data_editor
    column_config_dict = {
        #"task_id": None, # Hide task_id
        "task": st.column_config.TextColumn("Task Description", help="Edit the task description", width="large"),
        "created_date": st.column_config.DatetimeColumn("Created On", disabled=True, format="YYYY-MM-DD HH:mm:ss"),
        "completed": st.column_config.CheckboxColumn("Completed", help="Mark as completed"),
        "completed_date": st.column_config.DatetimeColumn("Completed On", disabled=True, format="YYYY-MM-DD HH:mm:ss"),
    }

    # Display data editor
    # The key is important for Streamlit to track changes
    edited_df = st.data_editor(
        df,
        column_config=column_config_dict,
        hide_index=True,
        width='content',
        # this key will create a dict to
        # store changes made using the dataframe editor
        key="update_data_editor"

    )

    # Check for changes and update database
    # st.session_state.update_data_editor will contain information about edited rows
    updates = st.session_state.update_data_editor['edited_rows']
    if st.button('Update Tasks') and updates: # Changed button label for clarity
        st.session_state['debug_messages'].append(f"{datetime.now().strftime('%H:%M:%S')} - DEBUG: --- 'Update' button clicked ---")
        st.session_state['debug_messages'].append(f"{datetime.now().strftime('%H:%M:%S')} - DEBUG: Detected updates from data_editor: {updates}")
        st.session_state.updated_tasks_count = 0
        
        for edited_row_index, changes in st.session_state.update_data_editor['edited_rows'].items():
            task_id = df.loc[edited_row_index, 'task_id']
            if pd.isna(task_id):
                st.session_state['debug_messages'].append(f"{datetime.now().strftime('%H:%M:%S')} - ERROR: task_id is NaN for edited row index {edited_row_index}. Skipping update.")
                st.error(f"Cannot update task: task_id is missing for row {edited_row_index}.")
                continue # Skip to next edited row

            # Get current values from the original dataframe for unchanged fields
            current_task_description = df.loc[edited_row_index, 'task']
            current_completed_status = df.loc[edited_row_index, 'completed']
            current_completed_date = df.loc[edited_row_index, 'completed_date']

            # Apply changes if they exist, otherwise keep current values
            new_task_description = changes.get('task', current_task_description)
            new_completed_status = changes.get('completed', current_completed_status)

            # Logic for completed_date based on new_completed_status
            new_completed_date = current_completed_date
            if 'completed' in changes: # Only update completed_date if completed status was changed
                new_completed_date = datetime.now() if new_completed_status else None

            st.session_state['debug_messages'].append(f"{datetime.now().strftime('%H:%M:%S')} - DEBUG:   Calling update_task_in_db for row {edited_row_index} (task_id: {task_id})")
            st.session_state['debug_messages'].append(f"{datetime.now().strftime('%H:%M:%S')} - DEBUG:     new_task_description: '{new_task_description}', new_completed_status: {new_completed_status}, new_completed_date: {new_completed_date}")
            if update_task_in_db(task_id, new_task_description, new_completed_status, new_completed_date):
                st.session_state.updated_tasks_count += 1
                st.session_state['debug_messages'].append(f"{datetime.now().strftime('%H:%M:%S')} - DEBUG:   Task {task_id} successfully processed for update.")
            else:
                st.session_state['debug_messages'].append(f"{datetime.now().strftime('%H:%M:%S')} - DEBUG:   Failed to update task {task_id}.")
        
        if st.session_state.updated_tasks_count > 0:
            st.session_state.data_version += 1 # Invalidate cache to force data reload
            st.session_state['success_update_message'] = True # Set flag to show success message
            st.rerun() # Rerun to show updated data and clear edited_rows

else:
    st.info("Your task list is empty. Use the 'Add a task' page to get started!")

# Display success message if an update just happened in the previous run
if st.session_state['success_update_message']:
    st.success(f"Successfully updated {st.session_state.updated_tasks_count} task(s).")
    st.session_state['success_update_message'] = False # Reset for next run