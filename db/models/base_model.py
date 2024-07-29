from db.db_connection import db_connect


class BaseModel:
    def __init__(self):
        self.conn = db_connect()
        self.cur = self.conn.cursor()

    def __del__(self):
        if self.conn is not None:
            self.cur.close()
            self.conn.close()
