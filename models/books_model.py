from db.db_connection import db_connect


class BooksModel:

    def __init__(self):
        self.ride_id = ''
        self.booked_places = ''
        self.passenger_name = ''
        self.passenger_id = ''

    def save_to_db(self):
        conn = db_connect()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO books (ride_id, booked_places, passenger_name, passenger_id)
            VALUES (%s, %s, %s, %s)
            """,
            (self.ride_id, self.booked_places, self.passenger_name, self.passenger_id)
        )
        cur.close()
        conn.commit()
        conn.close()

    @staticmethod
    def get_book(id):
        conn = db_connect()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM books
            WHERE id = %s
            """,
            id
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows


    @staticmethod
    def get_book_by_user(userId):
        conn = db_connect()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM books
            WHERE passenger_id = %s
            """,
            userId
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
