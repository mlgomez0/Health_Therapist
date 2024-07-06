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

def update_conversation(db_path, conversation_id, new_user_message=None, new_bot_response=None):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if new_user_message:
        cursor.execute('''
        UPDATE conversations
        SET user_message = ?, timestamp = ?
        WHERE id = ?
        ''', (new_user_message, datetime.datetime.now(), conversation_id))

    if new_bot_response:
        cursor.execute('''
        UPDATE conversations
        SET bot_response = ?, timestamp = ?
        WHERE id = ?
        ''', (new_bot_response, datetime.datetime.now(), conversation_id))

    conn.commit()
    conn.close()

    return f"Updated Conversation ID: {conversation_id}"

def query_conversations(db_path, user_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT * FROM conversations
    WHERE user_id = ?
    ORDER BY timestamp DESC
    ''', (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return rows

def check_conversation_exists(db_path, conversation_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT * FROM conversations
    WHERE id = ?
    ''', (conversation_id,))

    row = cursor.fetchone()
    conn.close()

    return row

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
            print("Usage: python test_db.py <db_path> create_conversation <user_id> <user_message> <bot_response>")
            sys.exit(1)
        user_id = int(sys.argv[3])
        user_message = sys.argv[4]
        bot_response = sys.argv[5]
        result = create_conversation(db_path, user_id, user_message, bot_response)
        print(result)
    elif method == "update_conversation":
        if len(sys.argv) < 4:
            print("Usage: python test_db.py <db_path> update_conversation <conversation_id> [<new_user_message>] [<new_bot_response>]")
            sys.exit(1)
        conversation_id = int(sys.argv[3])
        new_user_message = sys.argv[4] if len(sys.argv) > 4 else None
        new_bot_response = sys.argv[5] if len(sys.argv) > 5 else None
        result = update_conversation(db_path, conversation_id, new_user_message, new_bot_response)
        print(result)
    elif method == "query_conversations":
        if len(sys.argv) != 4:
            print("Usage: python test_db.py <db_path> query_conversations <user_id>")
            sys.exit(1)
        user_id = int(sys.argv[3])
        result = query_conversations(db_path, user_id)
        for row in result:
            print(row)
    elif method == "check_conversation_exists":
        if len(sys.argv) != 4:
            print("Usage: python test_db.py <db_path> check_conversation_exists <conversation_id>")
            sys.exit(1)
        conversation_id = int(sys.argv[3])
        result = check_conversation_exists(db_path, conversation_id)
        if result:
            print(f"Conversation exists: {result}")
        else:
            print(f"Conversation with ID {conversation_id} does not exist.")
    else:
        print(f"Unknown method: {method}")
        sys.exit(1)
