from typing import List
from .DbContext import DbContext
from src.domain.Conversation import Conversation
from pydantic import TypeAdapter
import json

class ConversationRepository():

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

    def get_conversations(self, user_id: int) -> List[Conversation]:
        sql = '''
            SELECT id, user_id, model_name, timestamp, user_score, user_feedback
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
                "timestamp": row[3],
                "user_score": row[4],
                "user_feedback": row[5]
            }
            conversations.append(Conversation(**conversation_data))
        
        return conversations
    
    
    def get_conversation_by_id(self, conversation_id: int):
        
        sql = '''
            SELECT * FROM conversations WHERE id = ?
        '''
        conversation = self.db.query_one(sql, (conversation_id,))
        print(conversation)

        sql = '''
            SELECT * FROM messages WHERE conversation_id = ?
        '''
        messages = self.db.query_all(sql, (conversation_id,))
        print(messages)

        return conversation, messages