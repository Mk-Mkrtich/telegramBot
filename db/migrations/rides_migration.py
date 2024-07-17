def create_rides_table():
    return """
        CREATE TABLE IF NOT EXISTS rides (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_name VARCHAR(255) NULL,
            user_id INT NULL,
            from_city VARCHAR(255) NOT NULL,
            to_city VARCHAR(255) NOT NULL,
            ride_date DATE NOT NULL,
            places INT NOT NULL,
            free_places INT NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            car_mark VARCHAR(255) NOT NULL,
            car_number VARCHAR(255) NOT NULL,
            car_color VARCHAR(255) NOT NULL
        )
        """