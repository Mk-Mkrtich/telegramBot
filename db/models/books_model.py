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

    def get_book(self, book_id):
        conn = db_connect()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM books
            join rides on (books.ride_id = rides.id)
            WHERE books.id = %s
            """,
            book_id
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row

    def get_books_by_user(self, userId):
        conn = db_connect()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM books
            join rides on (books.ride_id = rides.id)
            WHERE passenger_id = %s
            """,
            userId
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    def delete_book(self, book_id):
        conn = db_connect()
        cur = conn.cursor()
        cur.execute(
            """
            DELETE FROM books
            WHERE id = %s
            """,
            book_id
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
