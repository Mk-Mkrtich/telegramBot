from db.models.base_model import BaseModel


class BooksModel(BaseModel):

    def __init__(self):
        super().__init__()
        self.ride_id = ''
        self.booked_places = ''
        self.passenger_name = ''
        self.passenger_id = ''

    def save_to_db(self):
        self.cur.execute(
            """
            INSERT INTO books (ride_id, booked_places, passenger_name, passenger_id)
            VALUES (%s, %s, %s, %s)
            """,
            (self.ride_id, self.booked_places, self.passenger_name, self.passenger_id)
        )
        self.conn.commit()

    def get_book(self, book_id):
        self.cur.execute(
            """
            SELECT * FROM books
            join rides on (books.ride_id = rides.id)
            WHERE books.id = %s
            """,
            book_id
        )
        row = self.cur.fetchone()
        return row

    def get_books_by_user(self, userId):
        self.cur.execute(
            """
            SELECT * FROM books
            join rides on (books.ride_id = rides.id)
            WHERE passenger_id = %s
            """,
            userId
        )
        rows = self.cur.fetchall()
        return rows

    def delete_book(self, book_id):
        self.cur.execute(
            """
            DELETE FROM books
            WHERE id = %s
            """,
            book_id
        )
        self.conn.commit()
        return True

    def delete_bulk_books(self, book_ids):
        self.cur.execute(
            """
            DELETE FROM books
            WHERE IN id = %s
            """,
            book_ids
        )
        self.conn.commit()
        return True

    def __del__(self):
        super().__del__()

