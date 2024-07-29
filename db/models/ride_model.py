from db.models.base_model import BaseModel


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

    def get_matching_rides(self, from_city, to_city, date, free_places, limit=None):
        query = """
            SELECT * FROM rides
            WHERE from_city LIKE %s AND to_city LIKE %s AND ride_date = %s AND free_places >= %s
            """
        params = [from_city, to_city, date, free_places]
        if limit is not None:
            query += "LIMIT %s;"
            params.append(limit + 1)

        self.cur.execute(
            query,
            tuple(params)
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
            (id,)
        )
        row = self.cur.fetchone()
        return row

    def get_ride_list_by_user_id(self, user_id):
        self.cur.execute(
            """
            SELECT * FROM rides
            WHERE user_id = %s
            """,
            user_id
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

    def __del__(self):
        super().__del__()
