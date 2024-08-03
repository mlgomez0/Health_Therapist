from .DbContext import DbContext

class UserRepository:

    def __init__(self, db: DbContext):
        self.db = db

    def create_user(self, username: str, email: str, password: str):
        sql = '''
            INSERT INTO users (username, email, password) VALUES (?, ?, ?)
        '''
        return self.db.insert(sql, (username, email, password))

    def get_user_by_id(self, user_id: int):
        sql = '''
            SELECT * FROM users WHERE id = ?
        '''
        return self.db.query_one(sql, (user_id,))

    def get_user_by_username_or_email(self, username: str, email: str):
        sql = '''
            SELECT * FROM users WHERE username = ? OR email = ?
        '''
        return self.db.query_one(sql, (username, email))

    def get_user_by_username(self, username: str):
        sql = '''
            SELECT id, username, password, email FROM users WHERE username = ?
        '''
        row = self.db.query_one(sql, (username,))
        if row:
            return {
                "id": row[0],
                "username": row[1],
                "password": row[2],
                "email": row[3]
            }
        return None

    def update_user(self, user_id: int, new_username: str = None, new_email: str = None, new_password: str = None):
        if new_username:
            sql = '''
                UPDATE users
                SET username = ?
                WHERE id = ?
            '''
            self.db.execute_non_query(sql, (new_username, user_id))
        
        if new_email:
            sql = '''
                UPDATE users
                SET email = ?
                WHERE id = ?
            '''
            self.db.execute_non_query(sql, (new_email, user_id))
        
        if new_password:
            sql = '''
                UPDATE users
                SET password = ?
                WHERE id = ?
            '''
            self.db.execute_non_query(sql, (new_password, user_id))

        return f"Updated User ID: {user_id}"
    

    def insert_user(self, username: str, password: str) -> int:
        sql = '''
            INSERT INTO users (username, password) VALUES (?, ?)
        '''
        return self.db.insert(sql, (username, password))

    def update_user(self, user_id: int, username: str, password: str) -> int:
        sql = '''
            UPDATE users SET username = ?, password = ? WHERE id = ?
        '''
        return self.db.execute_non_query(sql, (username, password, user_id))


    def delete_user(self, user_id: int) -> int:
        sql = '''
            DELETE FROM users WHERE id = ?
        '''
        return self.db.execute_non_query(sql, (user_id,))
    
    def submit_feedback(self, user_id: int, conversation_id: int, feedback: str, rating: int):
        sql = '''
            INSERT INTO feedback (user_id, conversation_id, feedback, rating) VALUES (?, ?, ?, ?)
        '''
        return self.db.insert(sql, (user_id, conversation_id, feedback, rating))
