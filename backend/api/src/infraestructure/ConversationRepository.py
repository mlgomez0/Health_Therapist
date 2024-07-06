from typing import List
from .DbContext import DbContext
from src.domain.Conversation import Conversation
from pydantic import TypeAdapter
from src.domain.Message import Message

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

    def update_conversation(self, conversation_id: int, new_user_score: int = None, new_user_feedback: str = None):
        if new_user_score is not None:
            sql = '''
                UPDATE conversations
                SET user_score = ?, timestamp = CURRENT_TIMESTAMP
                WHERE id = ?
            '''
            self.db.execute_non_query(sql, (new_user_score, conversation_id))
        
        if new_user_feedback:
            sql = '''
                UPDATE conversations
                SET user_feedback = ?, timestamp = CURRENT_TIMESTAMP
                WHERE id = ?
            '''
            self.db.execute_non_query(sql, (new_user_feedback, conversation_id))

        return f"Updated Conversation ID: {conversation_id}"

    def get_conversations(self, user_id: int) -> List[dict]:
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
            conversations.append(conversation_data)
        
        return conversations
    
    def get_conversation_by_id(self, conversation_id: int):
        sql = '''
            SELECT * FROM conversations WHERE id = ?
        '''
        conversation = self.db.query_one(sql, (conversation_id,))
        
        sql = '''
            SELECT * FROM messages WHERE conversation_id = ?
        '''
        messages = self.db.query_all(sql, (conversation_id,)

        return conversation, messages
    
    def get_messages(self, conversation_id: int) -> List[Message]:
        
        sql = '''
            SELECT user_message, bot_response, timestamp FROM messages WHERE conversation_id = ?
        '''
        rows = self.db.query_all(sql, (conversation_id,))
        messages = []
        for row in rows:
            message_data = {
                "user_input": row[0],
                "bot_output": row[1],
                "datetime": row[2]
            }
            messages.append(Message(**message_data))
        return messages

