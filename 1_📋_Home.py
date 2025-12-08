# app.py - Página principal
import sqlite3
import streamlit as st
from db_path import DB_PATH
from debug import *

# The st.toggle widget itself manages st.session_state.debug_mode
st.toggle('Debug Mode', key='debug_mode')


# load the database
add_debug_message(f"DEBUG: DB_PATH used in app.py: {DB_PATH}")

conn = sqlite3.connect(DB_PATH, timeout=10)
cursor = conn.cursor()

# if database does not exist, create it
try:
    cursor.execute('SELECT 1 FROM tasks LIMIT 1;')

except:
    create_db_query = '''
    CREATE TABLE IF NOT EXISTS tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    created_date TEXT DEFAULT CURRENT_TIMESTAMP,
    completed_date TEXT,
    completed INTEGER DEFAULT 0
    )
    '''

    cursor.execute(create_db_query)
    conn.commit()

    add_debug_message(f'Database created successfully!')

finally:
    conn.close()

# Initialize session state variables that need to be shared across all pages
# This ensures they are available from the start of the user session.
if 'data_version' not in st.session_state:
    st.session_state.data_version = 0

if 'select_all_delete' not in st.session_state:
    st.session_state.select_all_delete = False

# Configurar la página
st.set_page_config(
    page_title="TODO Manager App",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título de la aplicación
st.title("📋 TODO List - Homepage")

st.write("Welcome to your personal TODO Tasks Manager!")
st.markdown("""
This application helps you manage your daily tasks efficiently. Here's what you can do:

- ➕ Use the ***Create tasks*** page to quickly create new tasks.
- 📋 View all your tasks in a clear list on the ***Read tasks*** page.
- 🔄 Modify existing tasks, mark them as completed, or change their descriptions on the ***Update tasks*** page.
- 🗑️ Remove tasks you no longer need from the ***Delete tasks*** page.

Stay organized and boost your productivity!
""")

# Display debug messages if debug mode is active
show_debug_messages()
