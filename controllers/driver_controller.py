from db.models.ride_model import RideModel
from controllers.base_controller import BaseController
import re
from components.start_buttons_component import generate_start_buttons
from components.price_buttons_component import generate_price_buttons


class DriverController(BaseController):
    def __init__(self, bot):
        super().__init__(bot)

    def set_places(self, message, places):
        if self.check_ignore("set_places_selection"):
            self.append_ignore("set_places_selection")
            self.ride.places = self.ride.free_places = places
            markup = generate_price_buttons()
            self.bot.send_message(message.chat.id, f"Selected places: {places}")
            self.bot.send_message(message.chat.id, "Write the price ֏ per passenger.", reply_markup=markup)

    def set_price(self, message, price):
        if self.check_ignore("set_price_selection"):
            self.append_ignore("set_price_selection")
            self.ride.price = price
            self.bot.send_message(message.chat.id, f"Selected price: {price}")
            self.bot.send_message(message.chat.id, "Write your car number.")
            self.bot.register_next_step_handler(message, self.set_car_number)

    def set_car_number(self, message):
        if self.check_ignore("set_car_number_selection"):
            pattern = re.compile(r'^\d{2,3}\s*[a-zA-Z]{2}\s*\d{2,3}$')

            if not pattern.match(message.text):
                self.bot.send_message(message.chat.id, "Try again: --> EXP: 123 AB 12 or 12 AB 123 <--",)
                self.bot.register_next_step_handler(message, self.set_car_number)
            else:
                self.append_ignore("set_car_number_selection")
                self.ride.car_number = message.text
                self.bot.send_message(message.chat.id, f"Your car mark: {message.text}")
                self.bot.send_message(message.chat.id, "Write your car mark.")
                self.bot.register_next_step_handler(message, self.set_car_mark)

    def set_car_mark(self, message):
        if self.check_ignore("set_car_mark_selection"):
            self.append_ignore("set_car_mark_selection")
            self.ride.car_mark = message.text
            self.bot.send_message(message.chat.id, f"Your car mark: {message.text}")
            self.bot.send_message(message.chat.id, "Write your car color.")
            self.bot.register_next_step_handler(message, self.set_car_color)

    def set_car_color(self, message):
        if self.check_ignore("set_car_color_selection"):
            self.append_ignore("set_car_color_selection")
            self.ride.car_color = message.text
            self.ride.user_name = message.from_user.username
            self.ride.user_id = message.from_user.id
            markup = generate_start_buttons(message)
            self.end_message_id = message.message_id
            self.clear_history(message.chat.id)
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

