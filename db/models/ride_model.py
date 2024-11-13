from admin.api_call import admin_call
from db.models.base_model import BaseModel
from db.models.pagination import Paginator


class RideModel:
    def __init__(self):
        self.from_city_id = ''
        self.to_city_id = ''
        self.date = ''
        self.time = ''
        self.places = ''
        self.free_places = ''
        self.price = ''
        self.baggage = ''
        self.car_id = ''
        self.user_id = ''

    def save_ride(self):
        new_ride = admin_call(self.__dict__, "tride/create", 'POST')
        return new_ride


