from db.db_connection import db_connect

class RideModel:
    def __init__(self):
        self.from_city = ''
        self.to_city = ''
        self.date = ''
        self.places = ''
        self.price = ''
        self.car_mark = ''
        self.car_number = ''
        self.car_color = ''
        self.user_name = ''

    def save_to_db(self):
        conn = db_connect()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO rides (from_city, to_city, ride_date, places, price, car_mark, car_number, car_color, user_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (self.from_city, self.to_city, self.date, self.places, self.price, self.car_mark, self.car_number, self.car_color, self.user_name)
        )
        cur.close()
        conn.commit()
        conn.close()

    @staticmethod
    def get_matching_rides(from_city, to_city, date, places):
        conn = db_connect()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM rides
            WHERE from_city LIKE %s AND to_city LIKE %s AND ride_date = %s AND places >= %s
            """,
            (from_city, to_city, date, places)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
