from telebot import types
from handlers.base_handler import BaseHandler
from models.ride_model import RideModel
from utils.city_utils import generate_city_buttons, cities
from utils.calendar_utils import generate_calendar_keyboard
import datetime

class PassengerHandler(BaseHandler):
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
            # self.bot.register_next_step_handler(callback.message, self.finish_ride_find)

    def finish_ride_find(self, message, places):
        self.ride.places = places
        rides = self.ride.get_matching_rides(self.ride.from_city, self.ride.to_city, self.ride.date, self.ride.places)
        if len(rides) == 0:
            return self.bot.send_message(message.chat.id, "No rides found.")
        rides_list = "OK, this is a list of rides. \n\n"
        for ride in rides:
            rides_list += (
                f"User - @{ride['user_name']}\n"
                f"From - {ride['from_city']}\n"
                f"To - {ride['to_city']}\n"
                f"Date - {ride['ride_date']}\n"
                f"Places - {str(ride['places'])}\n"
                f"Price - {str(ride['price'])}\n"
                f"Car - {ride['car_mark']} {ride['car_number']} color {ride['car_color']}\n\n"
            )
        self.bot.send_message(message.chat.id, rides_list)
        self.ride = RideModel()
