import sqlite3
import sys

def setup_database(db_path):
    # Connect to the SQLite3 database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_path)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Create a table to store users
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE
    )
    ''')

    # Create a table to store conversations
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        user_message TEXT NOT NULL,
        bot_response TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print("Database setup complete.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python setup_db.py <db_path>")
        sys.exit(1)

    db_path = sys.argv[1]
    setup_database(db_path)
