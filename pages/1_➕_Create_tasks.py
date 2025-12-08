import sqlite3
import streamlit as st
from time import sleep
from db_path import DB_PATH
from debug import *

if 'success_addition' not in st.session_state.keys():
    st.session_state['success_addition'] = False

if 'data_version' not in st.session_state.keys():
    st.session_state['data_version'] = 0

st.toggle('Debug Mode', key='debug_mode')

def create_task(task):
    add_debug_message(f"DEBUG: create_task function called with task: '{task}'")
    conn = sqlite3.connect(DB_PATH, timeout=10)
    add_debug_message(f"DEBUG: Database connection opened for creating task.")
    cursor = conn.cursor()

    try:
        create_task_query = '''
        INSERT INTO tasks (task) VALUES (?)
        '''
        add_debug_message(f"DEBUG: Executing INSERT query: {create_task_query} with param: ('{task}',)")

        # Parameters must be passed as a tuple, even for a single value
        cursor.execute(create_task_query, (task,))

        # Commit the transaction to save the changes
        conn.commit()
        st.session_state['success_addition'] = True
        add_debug_message(f"DEBUG: Task '{task}' added successfully and committed.")
    except Exception as e:
        add_debug_message(f"ERROR: Error creating task '{task}': {e}")
        st.error(f"Error adding task: {e}")
    finally:
        # Ensure the connection is closed even if an error occurs
        conn.close()
        st.session_state['task_text'] = ""
        add_debug_message(f"DEBUG: Database connection closed for creating task.")

st.header('Add a task to your list')

task = st.text_input('Create a new task', key = "task_text")

if st.button('Add task', on_click=create_task, args = (task,)):
    add_debug_message(f"DEBUG: 'Add task' button clicked.")
    if st.session_state['success_addition']:
        st.success('Task successfully added to your list!')
        st.session_state['success_addition'] = False
        st.session_state['data_version'] += 1
        add_debug_message(f"DEBUG: data_version incremented to {st.session_state['data_version']}.")
    sleep(1)
    st.rerun()
    add_debug_message(f"DEBUG: st.rerun() called after task addition.")

show_debug_messages()
