from admin.api_call import admin_call


class RideModel:
    def __init__(self):
        self.id = None
        self.from_city_id = None
        self.to_city_id = None
        self.date = None
        self.time = None
        self.places = None
        self.free_places = None
        self.price = None
        self.baggage = None
        self.car_id = None
        self.user_id = None
        self.action = None

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
