from backend.api.src.infraestructure.DbContext import DbContext


class ConversationRepository():

    def __init__(self, db: DbContext):
        self.db = db

    def create_conversation(self, user_id: int):
            
        sql = '''
            INSERT INTO conversations (user_id, timestamp) VALUES (?, CURRENT_TIMESTAMP)
        '''
        return self.db.execute_non_query(sql, (user_id,))
    
    def create_message(self, conversation_id: int, user_message: str, bot_response: str):
        
        sql = '''
            INSERT INTO messages (conversation_id, user_message, bot_response, timestamp) VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        '''
        return self.db.execute_non_query(sql, (conversation_id, user_message, bot_response))

    def get_conversations(self, user_id: int):
        
        sql = '''
            SELECT * FROM conversations WHERE user_id = ?
        '''
        return self.db.query_one(sql, (user_id,))
    
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