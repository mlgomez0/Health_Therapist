import sqlite3

def update_users_table(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    try:
        # Create a new table with the desired schema
        cursor.execute('''
            CREATE TABLE users_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        ''')
        
        # Copy the data from the old table to the new table
        cursor.execute('''
            INSERT INTO users_new (id, username, password)
            SELECT id, username, password FROM users
        ''')
        
        # Drop the old table
        cursor.execute('DROP TABLE users')
        
        # Rename the new table to the original name
        cursor.execute('ALTER TABLE users_new RENAME TO users')
        
        print("Schema updated successfully")
    except sqlite3.OperationalError as e:
        print(f"An error occurred: {e}")
    
    conn.commit()
    conn.close()

# Example usage
update_users_table('chat_data.db')
