from admin.api_call import admin_call
from .typed_model_attribute import TypedAttribute


class BookingsModel:

    def __init__(self):
        self.ride_id = TypedAttribute(int)
        self.places = TypedAttribute(int)
        self.passenger_id = TypedAttribute(int)
        self.id = TypedAttribute(int)

    def book_the_ride(self):
        return admin_call(self.__dict__, 'tride/booking/create', 'POST')

    def get_list(self):
        return admin_call(self.__dict__, 'tride/booking', 'POST')

    def get_book(self):
        return admin_call(self.__dict__, 'tride/booking/show', 'POST')

    def cancel_booking(self):
        return admin_call(self.__dict__, 'tride/booking/cancel', 'POST')

