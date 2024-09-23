import datetime

from db.models.base_model import BaseModel


class SupportModel(BaseModel):
    def __init__(self):
        super().__init__()
        self.user_id = ''
        self.user_name = ''
        self.support_message = ''
        self.date = datetime.datetime.now()
        self.status = 0

    def save_to_db(self):
        self.cur.execute(
            """
            INSERT INTO support_support (user_id, user_name, support_message, date, status)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (self.user_id, self.user_name, self.support_message, self.date, self.status)
        )
        self.conn.commit()

    def __del__(self):
        super().__del__()
