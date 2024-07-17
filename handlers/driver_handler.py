from telebot import types
from utils.city_utils import generate_city_buttons, cities
from utils.calendar_utils import generate_calendar_keyboard
from models.ride_model import RideModel
from handlers.base_handler import BaseHandler
import datetime
import re
from utils.start_buttons_utils import generate_start_buttons


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
            cities_clone = cities.copy()
            cities_clone.remove(city)
            markup = generate_city_buttons(cities_clone)
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
            markup = types.InlineKeyboardMarkup()
            passengers_count = []
            for i in range(1, 7):
                btn = types.InlineKeyboardButton(i, callback_data="passengersCount_" + str(i))
                passengers_count.append(btn)

            markup.row(*passengers_count)
            self.bot.send_message(callback.message.chat.id, "Please write the number of free places 👤.",
                                  reply_markup=markup)

    def set_places(self, message, places):
        self.ride.places = self.ride.free_places = places
        markup = types.InlineKeyboardMarkup()
        passengers_count = []
        for i in range(3, 8):
            btn = types.InlineKeyboardButton(str(i * 100) + " ֏", callback_data="priceData_" + str(i * 100))
            passengers_count.append(btn)
        markup.row(*passengers_count)
        passengers_count = []
        for i in range(8, 13):
            btn = types.InlineKeyboardButton(str(i * 100) + " ֏", callback_data="priceData_" + str(i * 100))
            passengers_count.append(btn)
        markup.row(*passengers_count)
        self.bot.send_message(message.chat.id, "Write the price ֏ per passenger.", reply_markup=markup)

    def set_price(self, message, price):
        self.ride.price = price
        self.bot.send_message(message.chat.id, "Write your car number.")
        self.bot.register_next_step_handler(message, self.set_car_number)

    def set_car_number(self, message):
        self.ride.car_number = message.text
        pattern = re.compile(r'^\d{2,3}\s*[a-zA-Z]{2}\s*\d{2,3}$')

        if not pattern.match(message.text):
            self.bot.send_message(message.chat.id, "Try again: --> EXP: 123 AB 12 or 12 AB 123 <--",)
            self.bot.register_next_step_handler(message, self.set_car_number)
        else:
            self.bot.send_message(message.chat.id, "Write your car mark.")
            self.bot.register_next_step_handler(message, self.set_car_mark)

    def set_car_mark(self, message):
        self.ride.car_mark = message.text
        self.bot.send_message(message.chat.id, "Write your car color.")
        self.bot.register_next_step_handler(message, self.set_car_color)

    def set_car_color(self, message):
        self.ride.car_color = message.text
        self.ride.user_name = message.from_user.username
        self.ride.user_id = message.from_user.id
        markup = generate_start_buttons(message)
        self.bot.send_message(message.chat.id, f"Ok, we registered your ride:\n\n"
                                               f"From - {self.ride.from_city}\n"
                                               f"To - {self.ride.to_city}\n"
                                               f"Date - {self.ride.date}\n"
                                               f"Places - {self.ride.free_places} / {self.ride.places}\n"
                                               f"Price - {self.ride.price}֏\n"
                                               f"🚙 {self.ride.car_color} {self.ride.car_mark} "
                                               f"{str(self.ride.car_number).upper().replace(" ", "")}",
                              reply_markup=markup)
        self.ride.save_to_db()
        self.ride = RideModel()

