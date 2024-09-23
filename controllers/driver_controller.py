from db.models.ride_model import RideModel
from controllers.base_controller import BaseController
import re
from components.price_buttons_component import generate_price_buttons
from components.car_collor_component import generate_color_buttons
from configs.storage import ids, start, finish, date, time, passenger, price, car, to_back, colors

class DriverController(BaseController):
    def __init__(self, bot):
        super().__init__(bot)

    def set_places(self, message, places):
        if self.check_ignore("set_places_selection_" + str(message.chat.id)):
            self.append_ignore("set_places_selection_" + str(message.chat.id))
            ids.add(message.message_id)
            self.ride.places = self.ride.free_places = places
            markup = generate_price_buttons()
            ids.add(self.bot.send_message(message.chat.id, f"Ընտրված ազատ տեղեր. {places}").id)
            ids.add(self.bot.send_message(message.chat.id, "Խնդրում ենք Ընտրեք արժեքը ֏ մեկ ուղևորի համար։", reply_markup=markup).id)

    def set_price(self, message, price):
        if self.check_ignore("set_price_selection_" + str(message.chat.id)):
            self.append_ignore("set_price_selection_" + str(message.chat.id))
            ids.add(message.message_id)
            self.ride.price = price
            ids.add(self.bot.send_message(message.chat.id, f"Ընտրված գինը. {price}").id)
            markup = generate_color_buttons()
            ids.add(self.bot.send_message(message.chat.id, "Խնդրում ենք Ընտրեք ձեր մեքենայի գույնը:", reply_markup=markup).id)

    def set_color(self, message, color):
        if self.check_ignore("set_color_selection_" + str(message.chat.id)):
            self.append_ignore("set_color_selection_" + str(message.chat.id))
            self.ride.car_color = color
            ids.add(self.bot.send_message(message.chat.id, f"Ընտրված գույն: {colors[color] + " " + color}").id)
            ids.add(self.bot.send_message(message.chat.id,  "Խնդրում ենք Գրեք ձեր մեքենայի մոդելը.").id)
            self.bot.register_next_step_handler(message, self.set_car_mark)

    def set_car_mark(self, message):
        if self.check_ignore("set_car_mark_selection_" + str(message.chat.id)):
            self.append_ignore("set_car_mark_selection_" + str(message.chat.id))
            ids.add(message.message_id)
            self.ride.car_mark = message.text
            ids.add(self.bot.send_message(message.chat.id, f"Ձեր մեքենայի մոդելը: {message.text}").id)
            ids.add(self.bot.send_message(message.chat.id, "Խնդրում ենք Գրեք ձեր մեքենայի պետ. համարըանիշը:").id)
            self.bot.register_next_step_handler(message, self.set_car_number)

    def set_car_number(self, message):
        if self.check_ignore("set_car_number_selection_" + str(message.chat.id)):
            pattern = re.compile(r'^\d{2,3}\s*[a-zA-Z]{2}\s*\d{2,3}$')

            if not pattern.match(message.text):
                ids.add(message.message_id)
                ids.add(self.bot.send_message(message.chat.id, "Կրկին փորձեք՝ --> օրինակ՝ 123 AB 12 կամ 12 AB 123 <--", ).id)
                self.bot.register_next_step_handler(message, self.set_car_number)
            else:
                self.append_ignore("set_car_number_selection_" + str(message.chat.id))
                ids.add(message.message_id)
                self.ride.car_number = message.text
                ids.add(self.bot.send_message(message.chat.id, f"Ձեր մեքենայի պետ. համարըանիշը: {message.text}").id)

                self.ride.user_name = message.from_user.username
                self.ride.user_id = message.from_user.id
                self.end_message_id = message.message_id
                self.clear_history(message.chat.id)
                self.bot.send_message(message.chat.id, f"Մենք գրանցեցինք ձեր ուղևորությունը:\n\n"
                                                       f"{start} {self.ride.from_city} "
                                                       f"{finish} {self.ride.to_city}\n"
                                                       f"{date} {self.ride.date} "
                                                       f"{time} {self.ride.ride_time}\n"
                                                       f"{passenger} {self.ride.places} Ազատ տեղ  \n"
                                                       f"{price} {self.ride.price}֏ դրամ\n"
                                                       f"{car} {self.ride.car_color} {self.ride.car_mark} "
                                                       f"{str(self.ride.car_number).upper().replace(" ", "")}"
                                                       f"\n\n\n"
                                                       f"Խնդրում եմ, հիշեք, որ գործ ունեք իրական մարդկանց հետ, "
                                                       f"խնդրում եմ մի ուշացեք, չեղարկեք ուղևորությունից 2 ժամ առաջ։ "
                                                       f"Եթե նկատում եք ուղևորների անընդունելի վարքագիծը,"
                                                       f" տեղեկացրեք մեզ:"
                                                       f"Գրեք հաղորդագրություն բոտին՝ նշելով ուղևորի օգտանունը "
                                                       f"'Telegram'- ում և բողոքի պատճառ")
                self.ride.save_to_db()
                self.ride = RideModel()

    def get_ride_list(self, message, action):
        data = self.ride_repo.ride_list(message.chat.id, action)
        ids.add(message.message_id)
        self.clear_history(message.chat.id)
        ids.add(self.bot.send_message(message.chat.id, data['rides_text'], reply_markup=data['markup']).id)

    def show_ride(self, message, id):
        ids.add(message.message_id)
        data = self.ride_repo.show_ride(id, "driver")
        ids.add(self.bot.send_message(message.chat.id, data['rides_text'], reply_markup=data['markup']).id)

    def cancel_ride(self, message, ride_id):
        self.ride_repo.cancel_ride_by_id(message, self.bot, ride_id)
        self.get_ride_list(message, "first")
