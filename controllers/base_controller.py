from repository.booking_repository import BookingRepository
from repository.ride_repository import RideRepository
from db.models.ride_model import RideModel
from components.calendar_component import CalendarComponent
from configs.cities import cities
from components.city_component import generate_city_buttons
import datetime


class BaseController:
    def __init__(self, bot):
        self.bot = bot
        self.ride = RideModel()
        self.book = BookingRepository(bot)
        self.calendar = CalendarComponent()
        self.ride_repo = RideRepository(bot)
        self.ignore_action = []
        self.start_message_id = 0
        self.end_message_id = 0

    def start(self, message):
        self.trash_ignore()
        if self.check_ignore("start_action"):
            self.start_message_id = message.message_id
            self.append_ignore("start_action")
            markup = generate_city_buttons(cities, "fromCity")
            self.bot.send_message(message.chat.id, "Cool, please select From where", reply_markup=markup)

    def handle_from_city_selection(self, message, city):
        self.role = ""
        if self.check_ignore("handle_from_city_selection_action"):
            self.append_ignore("handle_from_city_selection_action")
            self.ride.from_city = city
            cities_clone = cities.copy()
            cities_clone.remove(city)
            markup = generate_city_buttons(cities_clone, "toCity")
            self.bot.send_message(message.chat.id, f"Selected city: {city}")
            self.bot.send_message(message.chat.id, "Cool, please select To where", reply_markup=markup)


    def handle_to_city_selection(self, message, city):
        if self.check_ignore("handle_to_city_selection_action"):
            self.append_ignore("handle_to_city_selection_action")
            self.ride.to_city = city
            today = datetime.date.today()
            self.calendar.year = today.year
            self.calendar.month = today.month
            markup = self.calendar.generate_calendar_keyboard()
            self.bot.send_message(message.chat.id, f"Selected city: {city}")
            self.bot.send_message(message.chat.id, "Please select a date:", reply_markup=markup)

    def handle_calendar(self, callback):
        if self.check_ignore("handle_calendar_action"):
            data = self.calendar.handle_keyboard(self.bot, callback, self.ride)
            if data[0] == "edit":
                self.bot.edit_message_text("Please select a date:", callback.message.chat.id, callback.message.message_id,
                                           reply_markup=data[1])
            else:
                self.append_ignore("handle_calendar_action")
                self.bot.send_message(callback.message.chat.id, "Please write the number of free places 👤.",
                                          reply_markup=data[1])

    def check_ignore(self, action):
        if action in self.ignore_action:
            return False
        else:
            return True

    def append_ignore(self, action):
        self.ignore_action.append(action)

    def trash_ignore(self, ):
        self.ignore_action = []

    def clear_history(self, chat_id):
        ids = []
        for i in range(self.start_message_id, self.end_message_id + 1):
            ids.append(i)
        self.bot.delete_messages(chat_id, ids)
        self.start_message_id = 0
        self.end_message_id = 0
