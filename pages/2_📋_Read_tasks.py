import sqlite3
import streamlit as st
from streamlit import column_config
import pandas as pd
from db_path import DB_PATH
from debug import *

if 'data_version' not in st.session_state:
    st.session_state.data_version = 0

@st.cache_data
def read_tasks(data_version):
    conn = sqlite3.connect(DB_PATH, timeout=10)
    try:
        # Use pandas to read the SQL query directly into a DataFrame
        tasks_df = pd.read_sql_query("SELECT * FROM tasks ORDER BY created_date DESC", conn)
        
        # --- FIX: Convert columns to the correct data types ---
        # Convert the 'completed' column from 0/1 to boolean True/False
        tasks_df['completed'] = tasks_df['completed'].astype(bool)
        # Convert date-like strings to actual datetime objects for the data editor
        tasks_df['created_date'] = pd.to_datetime(tasks_df['created_date'])
        tasks_df['completed_date'] = pd.to_datetime(tasks_df['completed_date'], errors='coerce') # 'coerce' handles NULLs gracefully
        
        # hide task_id column
        tasks_df.drop('task_id', axis=1, inplace=True)

        return tasks_df
    except Exception as e:
        print(e)
        st.warning('Failed to read tasks from the database.')
        return pd.DataFrame() # Return an empty DataFrame on error
    finally:
        conn.close()

st.toggle('Debug mode', key='debug_mode')

st.header('Your List of Tasks')

tasks_df = read_tasks(st.session_state.data_version)

add_debug_message(f'DEBUG:   Tasks list retrieved from db')
add_debug_message(f'DEBUG:   Database file loaded from {DB_PATH}')

cfg = dict.fromkeys(tasks_df.columns)
cfg = {i: column_config.Column(width=None) for i in cfg.keys()}

if not tasks_df.empty:
    # Mostrar la tabla
    st.dataframe(tasks_df,
    column_config=cfg,
    width='content',  # Auto-ajuste al contenedor (default)
    hide_index=True
)
    
else:
    st.info("Your task list is empty. Use the 'Add a task' page to get started!")

# Display debug messages if debug mode is active
show_debug_messages()