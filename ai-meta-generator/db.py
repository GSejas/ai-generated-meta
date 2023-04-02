import sqlite3
import hashlib
from datetime import datetime

class ChatHistory:
    def __init__(self):
        self.connection = sqlite3.connect("chat_history.db")
        self.cursor = self.connection.cursor()
        self._initialize_db()

    def _initialize_db(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                query TEXT NOT NULL,
                response TEXT NOT NULL,
                model_settings TEXT NOT NULL
            );
        """)
        self.connection.commit()

    def add_history(self, query, response, model_settings):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        id = hashlib.md5((timestamp + query + response + model_settings).encode()).hexdigest()
        self.cursor.execute("INSERT INTO chat_history VALUES (?, ?, ?, ?, ?)", (id, timestamp, query, response, model_settings))
        self.connection.commit()

    def get_history_by_id(self, id):
        self.cursor.execute("SELECT * FROM chat_history WHERE id=?", (id,))
        return self.cursor.fetchone()

    def get_all_history(self):
        self.cursor.execute("SELECT * FROM chat_history")
        return self.cursor.fetchall()