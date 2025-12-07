import sqlite3
import streamlit as st
import pandas as pd

def read_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    success = False
    read_query = '''
    select * from tasks
    '''
    try:
        tasks_df = pd.read_sql_query(read_query, conn)
        tasks_df = tasks_df[['task', 'creation_date',
                            'completed', 'completed_date']]
        tasks_df['completed'] = tasks_df.completed.astype('str')
        tasks_df['completed'] = tasks_df.completed.apply(
            lambda x: '❌' if x == '0' else '✅')
    
        success = True
        # Use pandas to read the SQL query directly into a DataFrame
        tasks_df = pd.read_sql_query("SELECT * FROM tasks ORDER BY creation_date DESC", conn)
        # Convert the 'completed' column from 0/1 to boolean True/False
        tasks_df['completed'] = tasks_df['completed'].astype(bool)
        return tasks_df
    except Exception as e:
        print(e)

        st.warning('Failed to read tasks from the database.')
        return pd.DataFrame() # Return an empty DataFrame on error
    finally:
        conn.close()
        if not success:
            st.warning('Read operation failed!')
            return
        return tasks_df
    
st.write('Your list of tasks')

st.write(read_tasks())
st.header('Your List of Tasks')

tasks_df = read_tasks()

if not tasks_df.empty:
    edited_df = st.data_editor(
        tasks_df,
        column_config={
            "task_id": None, # Hide the task_id column
            "task": st.column_config.TextColumn("Task Description", width="large"),
            "creation_date": st.column_config.DatetimeColumn(
                "Created On",
                format="YYYY-MM-DD HH:mm:ss",
            ),
            "completed": st.column_config.CheckboxColumn("Status", default=False),
            "completed_date": st.column_config.DatetimeColumn(
                "Completed On",
                format="YYYY-MM-DD HH:mm:ss",
            ),
        },
        hide_index=True,
        use_container_width=True
    )
    # Here you would add logic to detect changes and update the database
else:
    st.info("Your task list is empty. Use the 'Add a task' page to get started!")