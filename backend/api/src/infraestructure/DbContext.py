import sqlite3
from typing import Any, List, Tuple

class DbContext:

    def __init__(self, db_name: str):
        self.db_name = db_name

        # If the database does not exist, create it
        if not self.database_exists():
            self.create_schema()

    def database_exists(self) -> bool:
        try:
            conn = self.connect()
            conn.close()
            return True
        except sqlite3.Error:
            return

    def connect(self):
        return sqlite3.connect(self.db_name)
    
    def create_schema(self):
        db = DbContext('data.db')
    
        # Create users table
        sql = '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        '''
        db.execute_non_query(sql, ())

        # Create conversations table
        sql = '''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_score INTEGER DEFAULT 0,
                user_feedback TEXT,
                CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users (id)
            )
        '''
        db.execute_non_query(sql, ())

        # Create conversations table
        sql = '''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                user_message TEXT NOT NULL,
                bot_response TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_conversation_id FOREIGN KEY (conversation_id) REFERENCES conversations (id)
            )
        '''
        db.execute_non_query(sql, ())
    
    def insert(self, query: str, values: Tuple[Any, ...]) -> int:
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            return cursor.lastrowid

    def execute_non_query(self, query: str, values: Tuple[Any, ...] = None) -> int:
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            return cursor.rowcount

    def query_one(self, query: str, values: Tuple[Any, ...]) -> Tuple[Any, ...]:
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            result = cursor.fetchone()
            return result

    def query_all(self, query: str, values: Tuple[Any, ...] = ()) -> List[Tuple[Any, ...]]:
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            results = cursor.fetchall()
            return results