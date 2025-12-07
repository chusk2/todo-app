import streamlit as st
import pandas as pd
import sqlite3

@st.cache_data
def load_tasks():
    conn = sqlite3.connect('tasks.db')
    try:
        df = pd.read_sql_query('SELECT task_id, task, creation_date FROM tasks ORDER BY creation_date DESC', conn)
    finally:
        conn.close()
    df['Seleccionar'] = False
    # Reorder columns to have 'Seleccionar' first
    df = df[['Seleccionar', 'task_id', 'task', 'creation_date']]
    return df

# Cargar datos
#df = load_tasks()

st.subheader("Lista de Tareas - Marca para eliminar")

# Configuración de la tabla editable
column_config = {
    "Seleccionar": st.column_config.CheckboxColumn(
        "Seleccionar para eliminar",
        help="Marca esta casilla si quieres eliminar la tarea",
        default=False,
    ),
    "task": st.column_config.TextColumn("Tarea", disabled=True),
    "creation_date": st.column_config.TextColumn("Fecha de Creación", disabled=True),
    "task_id" : None # Hide the task_id column
}

# Mostrar y editar la tabla
df_edited = st.data_editor(
    load_tasks(),
    column_config=column_config,
    use_container_width=True,
    hide_index=True,
)

# Botón para procesar eliminación
if st.button("Eliminar Tareas Seleccionadas"):
    df_selected = df_edited[df_edited['Seleccionar'] == True]

    if not df_selected.empty:
        selected_tasks_id = df_selected['task_id'].tolist()

        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        try:
            # Use a parameterized query to prevent SQL injection
            placeholders = ','.join('?' for _ in selected_tasks_id)
            query = f"DELETE FROM tasks WHERE task_id IN ({placeholders})"
            cursor.execute(query, selected_tasks_id)
            conn.commit()
            st.success(f"Se eliminaron {len(selected_tasks_id)} tarea(s) exitosamente.")
            st.cache_data.clear() # Clear the cache to force a data reload
        finally:
            conn.close()

        st.rerun()
    else:
        st.warning("No has seleccionado ninguna tarea. Marca las casillas deseadas.")

# Mostrar info adicional (opcional)
if not df_edited.empty:
    selected_tasks_count = (df_edited['Seleccionar'] == True).sum()
    st.info(f"Tareas seleccionadas para eliminar: {selected_tasks_count}")