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

    def finish_ride_find(self, message, places):
        self.ride.free_places = places
        self.handle_ride_find(message, 'first')


    def handle_ride_find(self, message, action):
        rides = self.ride.get_matching_rides(self.ride.from_city, self.ride.to_city, self.ride.date,
                                             self.ride.free_places)
        if len(rides) == 0:
            return self.bot.send_message(message.chat.id, "No rides found.")

        rides_text = ("OK, this is a list of rides. \n\n"
                      f"From - {self.ride.from_city}\n"
                      f"To - {self.ride.to_city}\n"
                      f"Date - {self.ride.date}\n"
                      f"Free places - {self.ride.free_places}")

        markup = types.InlineKeyboardMarkup()

        for ride in rides:
            btn = types.InlineKeyboardButton(f"Price - {str(ride['price'])}֏ "
                                             f" 🚙 {ride['car_color']} {ride['car_mark']} "
                                             f"{str(ride['car_number']).upper().replace(" ", "")} ",
                                             callback_data="showRide_" + str(ride['id']))
            markup.add(btn)
        if len(rides) > 10:
            first = types.InlineKeyboardButton("⬅️⬅️", callback_data="firstRides_first")
            prev = types.InlineKeyboardButton("⬅️️", callback_data="prevRides_prev")
            next = types.InlineKeyboardButton("➡️", callback_data="nextRides_next")
            last = types.InlineKeyboardButton("➡️➡️", callback_data="lastRides_last")
            markup.row(first, prev, next, last)

        self.bot.send_message(message.chat.id, rides_text, reply_markup=markup)


    def show_ride(self, message, id):
        ride = self.ride.find_matching_ride(id)
        if ride is None:
            return self.bot.send_message(message.chat.id, "Ride not found.")

        rides_text = (f"From - {ride['from_city']}\n"
                      f"To - {ride['to_city']}\n"
                      f"Date - {ride['ride_date']}\n"
                      f"Places - {ride['free_places']} / {ride['places']}\n"
                      f"Price - {ride['price']}֏\n"
                      f"🚙 - {ride['car_color']} {ride['car_mark']} "
                      f"{str(ride['car_number']).upper().replace(" ", "")}\n\n"
                      f"Select places count for BOOKING"
                      )

        markup = types.InlineKeyboardMarkup()
        places_count = []
        for i in range(1, int(ride['free_places']) + 1):
            btn = types.InlineKeyboardButton(str(i),
                                             callback_data="bookRide_" + str(ride['id']) + "_" + str(i))
            places_count.append(btn)

        markup.row(*places_count)
        back = types.InlineKeyboardButton("Back to list", callback_data="firstRides_first")
        markup.add(back)
        self.bot.send_message(message.chat.id, rides_text, reply_markup=markup)
