import datetime

from db.models.base_model import BaseModel


class UserModel(BaseModel):
    def __init__(self):
        super().__init__()
        self.user_id = ''
        self.user_name = ''
        self.bad_rating = ''
        self.blocked_until = datetime.datetime.now()

    def find_user(self):
        self.cur.execute(
            """
            SELECT * FROM botUsers_botusers
            WHERE user_id = %s 
            """,
            self.user_id
        )
        row = self.cur.fetchone()
        return row or None

    def create_user(self):
        self.cur.execute(
            """
            INSERT INTO botUsers_botusers (user_id, user_name, bad_rating, blocked_until)
            VALUES (%s, %s, %s, %s)
            """,
           ( self.user_id, self.user_name, self.bad_rating, self.blocked_until)
        )
        row = self.conn.commit()
        return row

    def __del__(self):
        super().__del__()
