import sys
import os

# Добавьте корневую директорию проекта в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from db.db_connection import db_connect

def create_driver_table():
    commands = (
        """
        CREATE TABLE IF NOT EXISTS rides (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_name VARCHAR(255) NULL,
            from_city VARCHAR(255) NOT NULL,
            to_city VARCHAR(255) NOT NULL,
            ride_date DATE NOT NULL,
            places INT NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            car_mark VARCHAR(255) NOT NULL,
            car_number VARCHAR(255) NOT NULL,
            car_color VARCHAR(255) NOT NULL
        )
        """
    )

    conn = None
    try:
        conn = db_connect()
        cur = conn.cursor()

        cur.execute(commands)

        cur.close()
        conn.commit()
        print("Tables created successfully.")

    except (Exception, pymysql.MySQLError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()
