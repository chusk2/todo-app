import sqlite3
import streamlit as st
import pandas as pd

def read_tasks():
    conn = sqlite3.connect('tasks.db')
    try:
        # Use pandas to read the SQL query directly into a DataFrame
        tasks_df = pd.read_sql_query("SELECT * FROM tasks ORDER BY creation_date DESC", conn)
        
        # --- FIX: Convert columns to the correct data types ---
        # Convert the 'completed' column from 0/1 to boolean True/False
        tasks_df['completed'] = tasks_df['completed'].astype(bool)
        # Convert date-like strings to actual datetime objects for the data editor
        tasks_df['creation_date'] = pd.to_datetime(tasks_df['creation_date'])
        tasks_df['completed_date'] = pd.to_datetime(tasks_df['completed_date'], errors='coerce') # 'coerce' handles NULLs gracefully
        
        return tasks_df
    except Exception as e:
        print(e)
        st.warning('Failed to read tasks from the database.')
        return pd.DataFrame() # Return an empty DataFrame on error
    finally:
        conn.close()

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