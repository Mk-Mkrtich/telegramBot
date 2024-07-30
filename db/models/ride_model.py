from db.models.base_model import BaseModel
from db.models.pagination import Paginator


class RideModel(BaseModel):
    def __init__(self):
        super().__init__()
        self.from_city = ''
        self.to_city = ''
        self.date = ''
        self.places = ''
        self.free_places = ''
        self.price = ''
        self.car_mark = ''
        self.car_number = ''
        self.car_color = ''
        self.user_name = ''
        self.user_id = ''
        self.table_name = "rides"
        self.page_size = 5
        self.paginator = Paginator(self.cur, self.table_name, self.page_size)

    def get_matching_rides(self, from_city, to_city, date, free_places, user_id, action="first"):
        if action == 'next':
            self.paginator.next_page()
        elif action == 'prev':
            self.paginator.prev_page()
        elif action == 'first':
            self.paginator.first_page()
        elif action == 'last':
            self.paginator.last_page()

        query = """
             SELECT * FROM rides
            WHERE from_city LIKE %s AND to_city LIKE %s AND ride_date = %s AND free_places >= %s AND user_id NOT LIKE %s
            """
        params = [from_city, to_city, date, free_places, user_id]
        self.cur.execute(
            query,
            params
        )
        count = self.cur.fetchall()
        if self.paginator.total_pages <= 0:
            self.paginator.update_total_pages(len(count))

        params.extend([self.page_size, self.paginator.offset])
        query += " ORDER BY id LIMIT %s OFFSET %s"
        self.cur.execute(
            query,
            params
        )
        rows = self.cur.fetchall()
        return rows

    def find_matching_ride(self, id):
        self.cur.execute(
            """
            SELECT * FROM rides
            WHERE id = %s 
            """,
            id
        )
        rows = self.cur.fetchone()
        return rows

    def update(self, id, place):
        self.cur.execute(
            """
            UPDATE rides
            SET free_places = %s
            WHERE id = %s
            """,
            (place, id)
        )
        self.conn.commit()
        self.cur.execute(
            """
            SELECT * FROM rides
            WHERE id = %s
            """,
            id
        )
        row = self.cur.fetchone()
        return row

    def get_ride_list_by_user_id(self, user_id, action="first"):
        if action == 'next':
            self.paginator.next_page()
        elif action == 'prev':
            self.paginator.prev_page()
        elif action == 'first':
            self.paginator.first_page()
        elif action == 'last':
            self.paginator.last_page()

        query = """
            SELECT * FROM rides
            WHERE user_id = %s
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
        query += " ORDER BY id LIMIT %s OFFSET %s"
        self.cur.execute(
            query,
            params
        )
        rows = self.cur.fetchall()
        return rows

    def get_ride_for_cancel(self, ride_id):
        self.cur.execute(
            """
            SELECT * FROM rides
            join books on (books.ride_id = rides.id)
            WHERE rides.id = %s
            """,
            ride_id
        )
        rows = self.cur.fetchall()
        return rows

    def delete_ride_by_id(self, ride_id):
        self.cur.execute(
            """
            DELETE FROM rides
            WHERE id = %s
            """,
            ride_id
        )
        self.conn.commit()
        return True

    def save_to_db(self):
        self.cur.execute(
            """
            INSERT INTO rides (from_city, to_city, ride_date, places, free_places, 
            price, car_mark, car_number, car_color, user_name, user_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (self.from_city, self.to_city, self.date, self.places, self.free_places,
             self.price, self.car_mark, self.car_number, self.car_color, self.user_name, self.user_id)
        )
        self.conn.commit()

    def __del__(self):
        super().__del__()
