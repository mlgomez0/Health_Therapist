from .DbContext import DbContext


class UserRepository():

    def __init__(self, db: DbContext):
        self.db = db

    def get_user_by_id(self, user_id):
        
        sql = '''
            SELECT * FROM users WHERE id = ?
        '''
        return self.db.query_one(sql, (user_id,))