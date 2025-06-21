import sqlite3
import json

def init_db():
    conn = sqlite3.connect('db/notes.db')
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            content TEXT,
            chunk_ids TEXT
        )
    '''
    )
    conn.commit()
    conn.close()

def save_note(user_id: int, content: str, chunk_ids: list):
    conn = sqlite3.connect('db/notes.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notes (user_id, content, chunk_ids) VALUES (?, ?, ?)",
        (user_id, content, json.dumps(chunk_ids))
    )
    conn.commit()
    conn.close()