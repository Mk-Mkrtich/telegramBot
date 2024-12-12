from admin.api_call import admin_call
from components.generate_cars_buttons import generate_cars_buttons
from db.models.car_model import CarModel
from db.models.ride_model import RideModel
from controllers.base_controller import BaseController
import re
from components.price_buttons_component import generate_price_buttons
from components.car_collor_component import generate_color_buttons
from components.baggage_component import generate_baggage_buttons
from configs.storage import ids, start, finish, date, time, passenger, price, car, colors, commandList


class BookingController(BaseController):
    def __init__(self, bot):
        super().__init__(bot)

    def booking_ride(self, message, ride_id, places):
        ids.add(message.message_id)
        self.clear_history(message.chat.id)
        self.booking.ride_id = ride_id
        self.booking.passenger_id = message.chat.id
        self.booking.places = places
        data = self.book_repo.book_ride(self.booking)
        self.bot.send_message(message.chat.id, data['text'])

    def get_booking_list(self, message):
        self.booking.passenger_id = message.chat.id
        data = self.book_repo.get_books_list(self.booking)
        self.clear_history(message.chat.id)
        self.trash_ignore(message.chat.id)
        ids.add(self.bot.send_message(message.chat.id, data['rides_text'], reply_markup=data['markup']).id)

    def show_booking(self, message, booking_id):
        self.booking.passenger_id = message.chat.id
        self.booking.id = booking_id
        data = self.book_repo.show_booking_details(self.booking)
        self.clear_history(message.chat.id)
        self.trash_ignore(message.chat.id)
        ids.add(self.bot.send_message(message.chat.id, data['rides_text'], reply_markup=data['markup']).id)

    def cancel_booking(self, message, booking_id):
        self.booking.id = booking_id
        data = self.book_repo.cancel(self.booking)
        self.clear_history(message.chat.id)
        self.trash_ignore(message.chat.id)
        ids.add(self.bot.send_message(message.chat.id, data['rides_text']).id)
