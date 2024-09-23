from db.models.base_model import BaseModel
from db.models.pagination import Paginator


class BooksModel(BaseModel, Paginator):

    def __init__(self):
        super().__init__()
        self.ride_id = ''
        self.booked_places = ''
        self.passenger_name = ''
        self.passenger_id = ''
        self.table_name = "books_book"
        self.page_size = 5
        self.paginator = Paginator(self.cur, self.table_name, self.page_size)

    def save_to_db(self):
        self.cur.execute(
            """
            INSERT INTO books_book (ride_id, booked_places, passenger_name, passenger_id)
            VALUES (%s, %s, %s, %s)
            """,
            (self.ride_id, self.booked_places, self.passenger_name, self.passenger_id)
        )
        self.conn.commit()

    def get_book(self, book_id):
        self.cur.execute(
            """
            SELECT * FROM books_book
            join rides_ride on (ride_id = rides_ride.id)
            WHERE books_book.id = %s
            """,
            book_id
        )
        row = self.cur.fetchone()
        return row

    def get_books_by_user(self, user_id, action):
        if action == 'next':
            self.paginator.next_page()
        elif action == 'prev':
            self.paginator.prev_page()
        elif action == 'first':
            self.paginator.first_page()
        elif action == 'last':
            self.paginator.last_page()

        query = """
            SELECT * FROM books_book
            join rides_ride on (ride_id = rides_ride.id)
            WHERE passenger_id = %s
        """
        params = [user_id]
        self.cur.execute(
            query,
            params
        )
        count = self.cur.fetchall()
        if self.paginator.total_pages <= 0:
            self.paginator.update_total_pages(len(count))

        params.extend([self.page_size, self.paginator.offset])
        query += " ORDER BY books_book.id LIMIT %s OFFSET %s"
        self.cur.execute(
            query,
            params
        )
        rows = self.cur.fetchall()
        return rows

    def delete_book(self, book_id):
        self.cur.execute(
            """
            DELETE FROM books_book
            WHERE id = %s
            """,
            book_id
        )
        self.conn.commit()
        return True

    def delete_bulk_books(self, book_ids):
        self.cur.execute(
            """
            DELETE FROM books_book
            WHERE IN id = %s
            """,
            book_ids
        )
        self.conn.commit()
        return True

    def __del__(self):
        super().__del__()

