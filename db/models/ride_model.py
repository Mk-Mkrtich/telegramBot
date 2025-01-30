from admin.api_call import admin_call
from db.models.typed_model_attribute import TypedAttribute


class RideModel:
    def __init__(self):
        self.id = TypedAttribute(int)
        self.from_city_id = TypedAttribute(int)
        self.to_city_id = TypedAttribute(int)
        self.date = TypedAttribute(str)
        self.time = TypedAttribute(str)
        self.places = TypedAttribute(int)
        self.free_places = TypedAttribute(int)
        self.price = TypedAttribute(int)
        self.baggage = TypedAttribute(bool)
        self.car_id = TypedAttribute(int)
        self.user_id = TypedAttribute(int)
        self.action = TypedAttribute(str)

    def save_ride(self):
        new_ride = admin_call(self.__dict__, "tride/create", 'POST')
        return new_ride

    def get_ride_list(self):
        ride_list = admin_call(self.__dict__, "tride/get", 'POST')
        print(ride_list)
        return ride_list

    def get_ride_by_id(self):
        ride_list = admin_call(self.__dict__, "tride/show", 'POST')
        print(ride_list)
        return ride_list

    def cancel_ride(self):
        ride_canceled = admin_call(self.__dict__, "tride/cancel", 'POST')
        print(ride_canceled)
        return ride_canceled
