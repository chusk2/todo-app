import sqlite3
import streamlit as st
import pandas as pd
from db_path import DB_PATH
from datetime import datetime

# Initialize session state variables
if 'data_version' not in st.session_state:
    st.session_state['data_version'] = 0

# This flag is used to show a success message after an update
if 'success_update_message' not in st.session_state:
    st.session_state['success_update_message'] = False

@st.cache_data
def load_tasks_from_db(data_version_for_cache_invalidation):
    """
    Loads tasks from the database.
    The data_version_for_cache_invalidation argument is used to invalidate the cache
    when tasks are added, updated, or deleted.
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query('SELECT task_id, task, creation_date, completed, completed_date FROM tasks ORDER BY creation_date DESC', conn)
        df['completed'] = df['completed'].astype(bool)
        # Ensure completed_date is datetime or None for proper display/editing
        # 'coerce' will turn invalid date strings (like NULL from DB) into NaT (Not a Time)
        df['completed_date'] = pd.to_datetime(df['completed_date'], errors='coerce')
        return df
    finally:
        conn.close()

def update_task_in_db(task_id, task_description, completed_status, completed_date):
    """
    Updates a single task in the database.
    completed_date should be a datetime object or None.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        # Convert boolean to integer for SQLite
        completed_int = 1 if completed_status else 0
        
        # Convert datetime to string for SQLite, or None if it's NaT or None
        completed_date_str = None
        if pd.notna(completed_date): # Check if it's a valid datetime (not NaT)
            completed_date_str = completed_date.strftime('%Y-%m-%d %H:%M:%S')

        update_query = '''
        UPDATE tasks
        SET task = ?, completed = ?, completed_date = ?
        WHERE task_id = ?
        '''
        cursor.execute(update_query, (task_description, completed_int, completed_date_str, task_id))
        conn.commit()
        return True # Indicate success
    except Exception as e:
        st.error(f"Error updating task {task_id}: {e}")
        return False # Indicate failure
    finally:
        conn.close()

st.header("📝 Update Your Tasks")

# Load tasks
try:
    df = load_tasks_from_db(st.session_state.data_version)
except Exception as e:
    st.error(f"Error loading tasks: {e}")
    df = pd.DataFrame() # Use an empty DataFrame on error

if not df.empty:
    # Define column configuration for st.data_editor
    column_config_dict = {
        "task_id": None, # Hide task_id
        "task": st.column_config.TextColumn("Task Description", help="Edit the task description", width="large"),
        "creation_date": st.column_config.DatetimeColumn("Created On", disabled=True, format="YYYY-MM-DD HH:mm:ss"),
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
        key="update_data_editor"
    )

    # Check for changes and update database
    # st.session_state.update_data_editor will contain information about edited rows
    if st.session_state.update_data_editor['edited_rows']:
        num_updated_tasks = 0
        
        for index, changes in st.session_state.update_data_editor['edited_rows'].items():
            task_id = df.loc[index, 'task_id']
            
            # Get current values from the original dataframe for unchanged fields
            current_task_description = df.loc[index, 'task']
            current_completed_status = df.loc[index, 'completed']
            current_completed_date = df.loc[index, 'completed_date']

            # Apply changes if they exist, otherwise keep current values
            new_task_description = changes.get('task', current_task_description)
            new_completed_status = changes.get('completed', current_completed_status)

            # Logic for completed_date based on new_completed_status
            new_completed_date = current_completed_date
            if 'completed' in changes: # Only update completed_date if completed status was changed
                new_completed_date = datetime.now() if new_completed_status else None

            if update_task_in_db(task_id, new_task_description, new_completed_status, new_completed_date):
                num_updated_tasks += 1
        
        if num_updated_tasks > 0:
            st.session_state.data_version += 1 # Invalidate cache to force data reload
            st.session_state['success_update_message'] = True # Set flag to show success message
            st.rerun() # Rerun to show updated data and clear edited_rows

else:
    st.info("Your task list is empty. Use the 'Add a task' page to get started!")

# Display success message if an update just happened in the previous run
if st.session_state['success_update_message']:
    st.success(f"Successfully updated task(s).")
    st.session_state['success_update_message'] = False # Reset for next run