import sqlite3
import streamlit as st

def create_task(task):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    success = False
    try:
        create_task_query = '''
        INSERT INTO tasks (task) VALUES (?)
        '''

        # Parameters must be passed as a tuple, even for a single value
        cursor.execute(create_task_query, (task,))

        # Commit the transaction to save the changes
        conn.commit()
        success = True
        print("Task added successfully!")
    finally:
        # Ensure the connection is closed even if an error occurs
        conn.close()
        if success:
            st.success('Task successfully added to your list!')

st.header('Add a task to your list')

task = st.text_input('Create a new task')

st.button('Add task', on_click=create_task, args = (task,))