def create_books_table():
    return """
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ride_id INT NOT NULL,
            booked_places INT NOT NULL,
            passenger_name VARCHAR(255) NULL,
            passenger_id INT NULL
        )
        """