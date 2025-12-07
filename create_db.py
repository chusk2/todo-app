import sqlite3

database = 'tasks.db'

conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

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

conn.close()

print(f'{database} created successfully!')