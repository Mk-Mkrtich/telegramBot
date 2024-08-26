from db.models.base_model import BaseModel

class CitiesModel(BaseModel):

    def __init__(self):
        super().__init__()
        self.table_name = "cities_cities"

    def get_cities(self):
        self.cur.execute(
            """
            SELECT `name` FROM cities_cities
            """,
        )
        rows = self.cur.fetchall()
        city_names = [row['name'] for row in rows]
        return city_names

    def __del__(self):
        super().__del__()