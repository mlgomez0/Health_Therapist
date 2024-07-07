import sqlite3
from typing import Any, List, Tuple
from colorama import Fore, init
import os

class DbContext:
    def __init__(self):
        # Use the correct path to your database
        self.db_name = os.path.join(os.path.dirname(__file__), 'chat_data.db')
        # If the database does not exist, create it
        if not os.path.exists(self.db_name):
            print(Fore.RED + 'Database does not exist')
            self.create_schema()
        else:
            print(Fore.MAGENTA + 'Database exists')

    def connect(self):
        return sqlite3.connect(self.db_name)

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

        # Create messages table
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
        print(Fore.MAGENTA + 'Messages table created')

    def execute_non_query(self, sql: str, params: Tuple[Any]):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()

    def query_one(self, sql: str, params: Tuple[Any]):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            return cursor.fetchone()

    def query_all(self, sql: str, params: Tuple[Any]):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            return cursor.fetchall()

    def insert(self, sql: str, params: Tuple[Any]):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            return cursor.lastrowid
