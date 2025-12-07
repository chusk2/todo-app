import streamlit as st
import pandas as pd
import sqlite3
from db_path import DB_PATH

@st.cache_data
def load_tasks_from_db(data_version):
    # This function will now raise an exception on failure, which is handled outside.
    conn = sqlite3.connect(DB_PATH, timeout=10) # Add a timeout to wait for DB lock release
    try:
        df = pd.read_sql_query('SELECT * FROM tasks ORDER BY creation_date DESC', conn)
        df['completed'] = df['completed'].astype(bool)
        return df
    finally:
        conn.close()

# Cargar datos
try:
    # Attempt to load data from the cached function
    df_from_db = load_tasks_from_db(st.session_state.data_version)
except Exception as e:
    # If loading fails, show an error and use an empty DataFrame for this run.
    # The failed result is NOT cached.
    st.error(f"Error loading tasks: {e}")
    df_from_db = pd.DataFrame()

# Create a copy to avoid modifying the cached object, which can raise an error
df = df_from_db.copy()

# Apply selection state AFTER loading from cache
df['Seleccionar'] = st.session_state.select_all_delete
original_cols = list(df_from_db.columns)
df = df[['Seleccionar'] + original_cols]

st.subheader("Lista de Tareas - Marca para eliminar")

# Define specific configurations for certain columns
# Ensure width=None is applied to all specific column configs
column_config_dict = {
    "Seleccionar": st.column_config.CheckboxColumn(
        "Seleccionar",
        help="Marca esta casilla si quieres eliminar la tarea",
        default=False,
        width=None,
    ),
    "task": st.column_config.TextColumn("Tarea", disabled=True, width=None),
    "creation_date": st.column_config.TextColumn("Fecha de Creación", disabled=True, width=None),
    "completed": st.column_config.CheckboxColumn("Completada", disabled=True, width=None),
    "task_id": None  # Hide the task_id column
}

# Build the final column_config dictionary, applying defaults where no specific config exists
# This loop ensures that every column gets a configuration, with width=None either explicitly
# set in specific_column_configs or as a default for other columns.

for col in df.columns:
    if col not in column_config_dict:
        column_config_dict[col] = st.column_config.Column(width=None)

# Mostrar y editar la tabla
df_renamed = st.data_editor(
    df,
    column_config=column_config_dict,
    width='content',
    hide_index=True,
    key="delete_data_editor" # Add a key for the data_editor
)

col1, col2 = st.columns([1, 2]) # Adjust columns for the new layout

with col1:
# Botón para procesar eliminación
    if st.button("Eliminar tareas"):
        df_selected = df_renamed[df_renamed['Seleccionar'] == True]

        if not df_selected.empty:
            selected_tasks_id_list = df_selected['task_id'].tolist()

            conn = sqlite3.connect(DB_PATH, timeout=10) # Add a timeout here as well for consistency
            cursor = conn.cursor()
            try:
                # Use a parameterized query to prevent SQL injection
                placeholders = ','.join('?' for _ in selected_tasks_id_list)
                query = f"DELETE FROM tasks WHERE task_id IN ({placeholders})"
                cursor.execute(query, selected_tasks_id_list)
                conn.commit()
                st.success(f"Se eliminaron {len(selected_tasks_id_list)} tarea(s) exitosamente.")
                st.session_state.data_version += 1 # Increment data version to invalidate cache
            finally:
                conn.close()

            st.rerun()
        else:
            st.warning("No has seleccionado ninguna tarea. Marca las casillas deseadas.")

with col2:
    # Use a single, stateful toggle for a cleaner UI and more robust state management
    new_select_all_state = st.toggle(
        'Seleccionar / Deseleccionar todo',
        value=st.session_state.select_all_delete,
        key='select_all_toggle'
    )
    # If the user changes the toggle, update the session state and rerun the app
    if new_select_all_state != st.session_state.select_all_delete:
        st.session_state.select_all_delete = new_select_all_state
        st.rerun()

# Mostrar info adicional (opcional)
selected_tasks_count = (df_renamed['Seleccionar'] == True).sum()
if selected_tasks_count > 0:
    st.info(f"Tareas seleccionadas para eliminar: {selected_tasks_count}")
