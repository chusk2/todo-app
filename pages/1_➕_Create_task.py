import sqlite3
import streamlit as st
from time import sleep
from db_path import DB_PATH

if 'success_addition' not in st.session_state.keys():
    st.session_state['success_addition'] = False

def create_task(task):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        create_task_query = '''
        INSERT INTO tasks (task) VALUES (?)
        '''

        # Parameters must be passed as a tuple, even for a single value
        cursor.execute(create_task_query, (task,))

        # Commit the transaction to save the changes
        conn.commit()
        st.session_state['success_addition'] = True
        print("Task added successfully!")
    finally:
        # Ensure the connection is closed even if an error occurs
        conn.close()
        st.session_state['task_text'] = ""

st.header('Add a task to your list')

task = st.text_input('Create a new task', key = "task_text")

if st.button('Add task', on_click=create_task, args = (task,)):
    if st.session_state['success_addition']:
        st.success('Task successfully added to your list!')
        st.session_state['success_addition'] = False
    sleep(1.5)
    st.rerun()

