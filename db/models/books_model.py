from admin.api_call import admin_call


class BookingsModel:

    def __init__(self):
        self.ride_id = None
        self.places = None
        self.passenger_id = None

    def book_the_ride(self):
        return admin_call(self.__dict__, 'tride/booking/create', 'POST')

