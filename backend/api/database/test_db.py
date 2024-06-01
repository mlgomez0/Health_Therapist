import sqlite3
import sys
import datetime

def create_user(db_path, username):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO users (username) VALUES (?)
    ''', (username,))

    user_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return f"User ID: {user_id}"

def create_conversation(db_path, user_id, user_message, bot_response):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO conversations (user_id, user_message, bot_response, timestamp) VALUES (?, ?, ?, ?)
    ''', (user_id, user_message, bot_response, datetime.datetime.now()))

    conversation_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return f"Conversation ID: {conversation_id}"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python test_db.py <db_path> <method> [args]")
        sys.exit(1)

    db_path = sys.argv[1]
    method = sys.argv[2]

    if method == "create_user":
        if len(sys.argv) != 4:
            print("Usage: python test_db.py <db_path> create_user <username>")
            sys.exit(1)
        username = sys.argv[3]
        result = create_user(db_path, username)
        print(result)
    elif method == "create_conversation":
        if len(sys.argv) != 6:
            print("Usage: python test_chatbot_database.py <db_path> create_conversation <user_id> <user_message> <bot_response>")
            sys.exit(1)
        user_id = int(sys.argv[3])
        user_message = sys.argv[4]
        bot_response = sys.argv[5]
        result = create_conversation(db_path, user_id, user_message, bot_response)
        print(result)
    else:
        print(f"Unknown method: {method}")
        sys.exit(1)