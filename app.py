# app.py - Página principal
import sqlite3
import streamlit as st
from db_path import DB_PATH
# from scripts.create import create
# from scripts.read import read
# from scripts.delete import delete

# load the database
conn = sqlite3.connect(DB_PATH, timeout=10)
cursor = conn.cursor()

try:
    cursor.execute('SELECT 1 FROM tasks LIMIT 1;')

except:
    create_db_query = '''
    CREATE TABLE IF NOT EXISTS tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    creation_date TEXT DEFAULT CURRENT_TIMESTAMP,
    completed_date TEXT,
    completed INTEGER DEFAULT 0
    )
    '''

    cursor.execute(create_db_query)
    conn.commit()

    print(f'Database created successfully!')

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
st.write("TODO Tasks Manager")

# # execute the home action or the previously selected one
# if not 'action' in st.session_state.keys():
#     st.session_state['action'] = home()

# st.session_state['action']


# pages = {
#     'create': {'subtitle' : 'Create a new task', 'fun' : create},
#     'read' : {'subtitle': 'View all your tasks', 'fun' : read },
#     'update': {'subtitle' : 'Edit an existing task', 'fun' : None },
#     'delete': {'subtitle' : 'Remove tasks from the list', 'fun' : delete }
# }

# for key, value in pages.items():
#     st.sidebar.markdown(f"### {value['subtitle']}")
    
#     if st.sidebar.button(label=f'{key.title()}', use_container_width=True):
#         st.session_state['current_page'] = f"{key}"
#         st.session_state['action'] = value['fun']()
#         value['fun']()
        
    
#     st.sidebar.divider()
