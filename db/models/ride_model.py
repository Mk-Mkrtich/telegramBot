from db.db_connection import db_connect


class RideModel:
    def __init__(self):
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
        conn = db_connect()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO rides (from_city, to_city, ride_date, places, free_places, 
            price, car_mark, car_number, car_color, user_name, user_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (self.from_city, self.to_city, self.date, self.places, self.free_places,
             self.price, self.car_mark, self.car_number, self.car_color, self.user_name, self.user_id)
        )
        cur.close()
        conn.commit()
        conn.close()

    def get_matching_rides(self, from_city, to_city, date, free_places):
        conn = db_connect()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM rides
            WHERE from_city LIKE %s AND to_city LIKE %s AND ride_date = %s AND free_places >= %s
            """,
            (from_city, to_city, date, free_places)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    def find_matching_ride(self, id):
        conn = db_connect()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM rides
            WHERE id = %s 
            """,
            id
        )
        rows = cur.fetchone()
        cur.close()
        conn.close()
        return rows

    def update(self, id, place):
        conn = db_connect()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                UPDATE rides
                SET free_places = %s
                WHERE id = %s
                """,
                (place, id)
            )
            conn.commit()
            cur.execute(
                """
                SELECT * FROM rides
                WHERE id = %s
                """,
                (id,)
            )
            row = cur.fetchone()
        finally:
            cur.close()
            conn.close()
        return row

    def get_ride_list_by_user_id(self, user_id):
        conn = db_connect()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM rides
            WHERE user_id = %s
            """,
            user_id
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
