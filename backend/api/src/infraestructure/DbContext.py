import sqlite3
from typing import Any, List, Tuple
from colorama import Fore, init
import os

class DbContext:

    def __init__(self):

        self.db_name = 'chat_data.db'
        # If the database does not exist, create it
        if not os.path.exists(self.db_name):
            print(Fore.RED + 'Database does not exist')
            self.create_schema()
        else:
            print(Fore.MAGENTA + 'Database exists')

    def connect(self):
        return sqlite3.connect(self.db_name,)
    
    def create_schema(self):

        # Create users table
        sql = '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        '''
        self.execute_non_query(sql, ())
        print(Fore.MAGENTA + 'Users table created')

        # Create conversations table
        sql = '''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                model_name TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_score INTEGER DEFAULT 0,
                user_feedback TEXT,
                CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users (id)
            )
        '''
        self.execute_non_query(sql, ())
        print(Fore.MAGENTA + 'Conversations table created')

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
        self.execute_non_query(sql, ())

        # Create default user if not exists
        sql = '''
            INSERT OR IGNORE INTO users (username, password) VALUES (?, ?);
        '''
        self.insert(sql, ('admin', 'admin'))
        print(Fore.MAGENTA + 'Default user created')






    
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