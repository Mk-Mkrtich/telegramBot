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


class DriverController(BaseController):
    def __init__(self, bot):
        super().__init__(bot)

    def set_places(self, message, places):
        if self.check_ignore("set_places_selection_" + str(message.chat.id)):
            self.append_ignore("set_places_selection_" + str(message.chat.id))
            ids.add(message.message_id)
            self.ride.places = self.ride.free_places = places
            markup = generate_baggage_buttons()
            ids.add(self.bot.send_message(message.chat.id, f"Ընտրված ազատ տեղեր. {places}").id)
            ids.add(self.bot.send_message(message.chat.id, "xndrum enq ynterl uxeberi arkayutyuny", reply_markup=markup).id)

    def set_baggage(self, message, baggage):
        if self.check_ignore("set_baggage_" + str(message.chat.id)):
            self.append_ignore("set_baggage_" + str(message.chat.id))
            ids.add(message.message_id)
            self.ride.baggage = (baggage == 'yes')
            markup = generate_price_buttons()
            ids.add(self.bot.send_message(message.chat.id, "Խնդրում ենք Ընտրեք արժեքը ֏ մեկ ուղևորի համար։",
                                          reply_markup=markup).id)

    def set_price(self, message, price):
        if self.check_ignore("set_price_selection_" + str(message.chat.id)):
            self.append_ignore("set_price_selection_" + str(message.chat.id))
            ids.add(message.message_id)
            self.ride.price = price
            ids.add(self.bot.send_message(message.chat.id, f"Ընտրված գինը. {price}").id)

            self.car.tuid = message.chat.id
            cars = self.car.get_car()['data']
            print(cars, 'cars data')
            if cars:
                markup = generate_cars_buttons(cars)
                ids.add(self.bot.send_message(message.chat.id, "testttttttttttttւ", reply_markup=markup).id)
            else:
                markup = generate_color_buttons()
                ids.add(self.bot.send_message(message.chat.id, "Խնդրում ենք Ընտրեք ձեր մեքենայի գույնը:", reply_markup=markup).id)

    def set_new_car(self, message, user_id):
        if self.check_ignore("set_new_car" + str(message.chat.id)):
            self.append_ignore("set_new_car" + str(message.chat.id))
            ids.add(message.message_id)
            self.ride.user_id = user_id
            markup = generate_color_buttons()
            ids.add(self.bot.send_message(message.chat.id, "Խնդրում ենք Ընտրեք ձեր մեքենայի գույնը:", reply_markup=markup).id)

    def set_color(self, message, color):
        if self.check_ignore("set_color_selection_" + str(message.chat.id)):
            self.append_ignore("set_color_selection_" + str(message.chat.id))
            self.car.color = color
            ids.add(self.bot.send_message(message.chat.id, f"Ընտրված գույն: {colors[color] + " " + color}").id)
            ids.add(self.bot.send_message(message.chat.id,  "Խնդրում ենք Գրեք ձեր մեքենայի մոդելը.").id)
            self.bot.register_next_step_handler(message, self.set_car_mark)

    def set_car_mark(self, message):
        if self.check_ignore("set_car_mark_selection_" + str(message.chat.id)):
            self.append_ignore("set_car_mark_selection_" + str(message.chat.id))
            command = message.text[1:]
            if command in commandList:
                return self.bot.send_message(message.chat.id, 'Դուք դադարեցրել եք գործողությունը,'
                                                              f' խնդրում ենք կրկին ուղարկել /{command} հրամանը մեկ'
                                                              f' այլ գործողություն սկսելու համար')
            ids.add(message.message_id)
            self.car.model = message.text
            ids.add(self.bot.send_message(message.chat.id, f"Ձեր մեքենայի մոդելը: {message.text}").id)
            ids.add(self.bot.send_message(message.chat.id, "Խնդրում ենք Գրեք ձեր մեքենայի պետ. համարըանիշը:").id)
            self.bot.register_next_step_handler(message, self.set_car_number)

    def set_car_number(self, message):
        if self.check_ignore("set_car_number_selection_" + str(message.chat.id)):
            command = message.text[1:]
            if command in commandList:
                return self.bot.send_message(message.chat.id, 'Դուք դադարեցրել եք գործողությունը,'
                                                              f' խնդրում ենք կրկին ուղարկել /{command} հրամանը մեկ'
                                                              f' այլ գործողություն սկսելու համար')

            pattern = re.compile(r'^\d{2,3}\s*[a-zA-Z]{2}\s*\d{2,3}$')

            if not pattern.match(message.text):
                ids.add(message.message_id)
                ids.add(self.bot.send_message(message.chat.id, "Կրկին փորձեք՝ --> օրինակ՝ 123 AB 12 կամ 12 AB 123 <--", ).id)
                self.bot.register_next_step_handler(message, self.set_car_number)
            else:

                self.append_ignore("set_car_number_selection_" + str(message.chat.id))
                ids.add(message.message_id)
                ids.add(self.bot.send_message(message.chat.id, f"Ձեր մեքենայի պետ. համարըանիշը: {message.text}").id)

                self.car.number = message.text
                self.car.tuid = message.chat.id
                new_car_data = self.car.check_car()

                self.ride.car_id = new_car_data['data']['id']
                self.ride.user_id = new_car_data['data']['user_id']

                self.publish_ride(message)

                self.ride = RideModel()
                self.car = CarModel()

    def publish_ride(self, message, car_id=None, user_id=None):
        if self.check_ignore("publish_ride" + str(message.chat.id)):
            self.append_ignore("publish_ride" + str(message.chat.id))
            if car_id is not None and user_id is not None:
                self.ride.car_id = car_id
                self.ride.user_id = user_id

            ride = self.ride.save_ride()
            self.clear_history(message.chat.id)
            if ride['code'] == 401:
                self.bot.send_message(message.chat.id,
                                      f"uxevorutyunneri mijev petq e lini mininimum mek jam tarberutyun :")
            elif ride['code'] == 201:
                self.bot.send_message(message.chat.id, f"Մենք գրանցեցինք ձեր ուղևորությունը:")
            else:
                self.bot.send_message(message.chat.id, f"arka e texnikakan xndir, xndrum enq porcel mi poqr ush")

    #
    # def show_ride(self, message, id):
    #     ids.add(message.message_id)
    #     data = self.ride_repo.show_ride(id, "driver")
    #     ids.add(self.bot.send_message(message.chat.id, data['rides_text'], reply_markup=data['markup']).id)
    #
    # def cancel_ride(self, message, ride_id):
    #     self.ride_repo.cancel_ride_by_id(message, self.bot, ride_id)
    #     self.get_ride_list(message, "first")
