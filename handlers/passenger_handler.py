from telebot import types
from handlers.base_handler import BaseHandler
from models.ride_model import RideModel
from utils.city_utils import generate_city_buttons, cities

class PassengerHandler(BaseHandler):
    def __init__(self, bot):
        super().__init__(bot)
        self.ride = RideModel()

    def start(self, message):
        markup = generate_city_buttons(cities)
        self.bot.send_message(message.chat.id, "Cool, please select From where", reply_markup=markup)

    def find_from_city(self, message):
        self.find_from_city = message.text
        self.bot.send_message(message.chat.id, "Write from where you want to travel?")
        self.bot.register_next_step_handler(message, self.find_to_city)

    def find_to_city(self, message):
        self.find_to_city = message.text
        self.bot.send_message(message.chat.id, "Write to where you want to travel?")
        self.bot.register_next_step_handler(message, self.find_date)

    def find_date(self, message):
        self.find_date = message.text
        self.bot.send_message(message.chat.id, "Write when you want to travel?")
        self.bot.register_next_step_handler(message, self.find_places)

    def find_places(self, message):
        self.find_places = message.text
        self.bot.send_message(message.chat.id, "Write how many places you need?")
        self.bot.register_next_step_handler(message, self.finish_ride_find)

    def finish_ride_find(self, message):
        self.bot.send_message(message.chat.id, "OK, this is a list of rides.")
