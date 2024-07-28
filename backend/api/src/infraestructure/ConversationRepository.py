from typing import List
from .DbContext import DbContext

class ConversationRepository:
    def __init__(self, db: DbContext):
        self.db = db

    def create_conversation(self, user_id: int, model_name: str):
        sql = '''
            INSERT INTO conversations (user_id, model_name, timestamp) VALUES (?, ?, CURRENT_TIMESTAMP)
        '''
        return self.db.insert(sql, (user_id, model_name))
    
    def create_message(self, conversation_id: int, user_message: str, bot_response: str):
        sql = '''
            INSERT INTO messages (conversation_id, user_message, bot_response, timestamp) VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        '''
        return self.db.insert(sql, (conversation_id, user_message, bot_response))

    def update_summary(self, conversation_id: int, summary: str):
        sql = '''
            UPDATE conversations
            SET summary = ?
            WHERE id = ?
        '''
        self.db.execute_non_query(sql, (summary, conversation_id))

    def get_conversations(self, user_id: int) -> List[dict]:
        sql = '''
            SELECT id, user_id, model_name, summary, timestamp
            FROM conversations
            WHERE user_id = ?
        '''
        items = self.db.query_all(sql, (user_id,))
        
        conversations = []
        for row in items:
            conversation_data = {
                "id": row[0],
                "user_id": row[1],
                "model_name": row[2],
                "summary": row[3],
                "timestamp": row[4]
            }
            conversations.append(conversation_data)
        
        return conversations
    
    def get_conversation_by_id(self, conversation_id: int):
        sql = '''
            SELECT id, user_id, model_name, summary, timestamp
            FROM conversations WHERE id = ?
        '''
        conversation = self.db.query_one(sql, (conversation_id,))
        
        sql = '''
            SELECT id, conversation_id, user_message, bot_response, timestamp
            FROM messages WHERE conversation_id = ?
        '''
        messages = self.db.query_all(sql, (conversation_id,))
        
        return {
            "conversation": {
                "id": conversation[0],
                "user_id": conversation[1],
                "model_name": conversation[2],
                "summary": conversation[3],
                "timestamp": conversation[4]
            },
            "messages": [
                {
                    "id": message[0],
                    "conversation_id": message[1],
                    "user_message": message[2],
                    "bot_response": message[3],
                    "timestamp": message[4]
                }
                for message in messages
            ]
        }
