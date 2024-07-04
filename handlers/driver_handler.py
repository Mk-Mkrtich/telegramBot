from telebot import types
from utils.city_utils import generate_city_buttons, cities
from utils.calendar_utils import generate_calendar_keyboard
from models.ride_model import RideModel
from handlers.base_handler import BaseHandler
import datetime


class DriverHandler(BaseHandler):
    def __init__(self, bot):
        super().__init__(bot)
        self.ride = RideModel()

    def start(self, message):
        markup = generate_city_buttons(cities)
        self.bot.send_message(message.chat.id, "Cool, please select From where", reply_markup=markup)

    def handle_city_selection(self, message, city):
        if not self.ride.from_city:
            self.ride.from_city = city
            markup = generate_city_buttons(cities)
            self.bot.send_message(message.chat.id, "Cool, please select To where", reply_markup=markup)
        elif not self.ride.to_city:
            self.ride.to_city = city
            today = datetime.date.today()
            markup = generate_calendar_keyboard(today.year, today.month)
            self.bot.send_message(message.chat.id, "Please select a date:", reply_markup=markup)
        else:
            self.bot.send_message(message.chat.id, "City selection is complete. Please proceed to the next step.")

    def handle_calendar(self, callback):
        data = callback.data.split('_')
        if data[0] == 'prev' and data[1] == 'month':
            year, month = int(data[2]), int(data[3])
            month -= 1
            if month == 0:
                month = 12
                year -= 1
            markup = generate_calendar_keyboard(year, month)
            self.bot.edit_message_text("Please select a date:", callback.message.chat.id, callback.message.message_id,
                                       reply_markup=markup)
        elif data[0] == 'next' and data[1] == 'month':
            year, month = int(data[2]), int(data[3])
            month += 1
            if month == 13:
                month = 1
                year += 1
            markup = generate_calendar_keyboard(year, month)
            self.bot.edit_message_text("Please select a date:", callback.message.chat.id, callback.message.message_id,
                                       reply_markup=markup)
        elif data[0] == 'day':
            year, month, day = int(data[1]), int(data[2]), int(data[3])
            self.ride.date = f"{year}-{month:02}-{day:02}"
            self.bot.send_message(callback.message.chat.id, f"Selected date: {self.ride.date}")
            self.bot.send_message(callback.message.chat.id, "Please write the number of free places 👤.")
            self.bot.register_next_step_handler(callback.message, self.set_places)

    def set_places(self, message):
        self.ride.places = message.text
        self.bot.send_message(message.chat.id, "Write the price ֏ per passenger.")
        self.bot.register_next_step_handler(message, self.set_price)

    def set_price(self, message):
        self.ride.price = message.text
        self.bot.send_message(message.chat.id, "Write your car number.")
        self.bot.register_next_step_handler(message, self.set_car_number)

    def set_car_number(self, message):
        self.ride.car_number = message.text
        self.bot.send_message(message.chat.id, "Write your car mark.")
        self.bot.register_next_step_handler(message, self.set_car_mark)

    def set_car_mark(self, message):
        self.ride.car_mark = message.text
        self.bot.send_message(message.chat.id, "Write your car color.")
        self.bot.register_next_step_handler(message, self.set_car_color)

    def set_car_color(self, message):
        self.ride.car_color = message.text
        self.ride.user_name = message.from_user.username
        self.bot.send_message(message.chat.id, f"Ok, we registered your ride:\n"
                                               f"From - {self.ride.from_city}\n"
                                               f"To - {self.ride.to_city}\n"
                                               f"Date - {self.ride.date}\n"
                                               f"Places - {self.ride.places}\n"
                                               f"Price - {self.ride.price}\n"
                                               f"Car - {self.ride.car_mark} {self.ride.car_number}, color {self.ride.car_color}")
        self.ride.save_to_db()
