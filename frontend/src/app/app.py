from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('my_database.db')  # Ensure this matches the database created by setup_db.py
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/conversations/<int:user_id>', methods=['GET'])
def get_conversations(user_id):
    conn = get_db_connection()
    conversations = conn.execute('SELECT * FROM conversations WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in conversations])

@app.route('/conversation/<int:conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    conn = get_db_connection()
    conversation = conn.execute('SELECT * FROM conversations WHERE id = ?', (conversation_id,)).fetchone()
    messages = conn.execute('SELECT * FROM messages WHERE conversation_id = ?', (conversation_id,)).fetchall()
    conn.close()
    return jsonify({
        'conversation': dict(conversation),
        'messages': [dict(message) for message in messages]
    })

@app.route('/add_conversation', methods=['POST'])
def add_conversation():
    data = request.get_json()
    user_id = data['user_id']
    user_message = data['user_message']
    bot_response = data['bot_response']
    summary = data['summary']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO conversations (user_id, user_message, bot_response, summary, timestamp)
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
    ''', (user_id, user_message, bot_response, summary))
    conn.commit()
    conversation_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'conversation_id': conversation_id})

if __name__ == '__main__':
    app.run(debug=True)
