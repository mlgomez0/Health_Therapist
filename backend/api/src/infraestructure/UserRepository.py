from .DbContext import DbContext

class UserRepository:

    def __init__(self, db: DbContext):
        self.db = db

    def create_user(self, username: str, password: str):
        sql = '''
            INSERT INTO users (username, password) VALUES (?, ?)
        '''
        return self.db.insert(sql, (username, password))

    def get_user_by_id(self, user_id: int):
        sql = '''
            SELECT * FROM users WHERE id = ?
        '''
        return self.db.query_one(sql, (user_id,))

    def update_user(self, user_id: int, new_username: str = None, new_password: str = None):
        if new_username:
            sql = '''
                UPDATE users
                SET username = ?
                WHERE id = ?
            '''
            self.db.execute_non_query(sql, (new_username, user_id))
        
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
