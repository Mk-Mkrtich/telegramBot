from telebot import types

from components.paginate_buttons_component import generate
from db.models.ride_model import RideModel


class RideRepository:

    def __init__(self, bot):
        self.ride = RideModel()
        self.bot = bot

    def show_ride(self, message, id, role):
        ride = self.ride.find_matching_ride(id)
        markup = types.InlineKeyboardMarkup()

        if ride is None:
            return {"markup": markup, "rides_text": "Ride not found."}

        rides_text = (f"From - {ride['from_city']}\n"
                      f"To - {ride['to_city']}\n"
                      f"Date - {ride['ride_date']}\n"
                      f"Places - {ride['free_places']} / {ride['places']}\n"
                      f"Price - {ride['price']}֏\n"
                      f"🚙 - {ride['car_color']} {ride['car_mark']} "
                      f"{str(ride['car_number']).upper().replace(" ", "")}\n\n"
                      )

        if ride['user_id'] != message.chat.id:
            rides_text += f"Select places count for BOOKING"
            places_count = []
            for i in range(1, int(ride['free_places']) + 1):
                btn = types.InlineKeyboardButton(str(i),
                                                 callback_data="bookRide_" + str(ride['id']) + "_" + str(i))
                places_count.append(btn)

            markup.row(*places_count)
        if role == "passenger":
            back = types.InlineKeyboardButton("Back to list", callback_data="rides_first")
        else:
            back = types.InlineKeyboardButton("Back to list", callback_data="ridesList_first")
            cancel = types.InlineKeyboardButton("Cancel the ride", callback_data="cancelRide_" + str(id))
            markup.add(cancel)

        markup.add(back)
        return {"markup": markup, "rides_text": rides_text}

    def find_ride(self, data):
        find_data = [data['from_city'], data['to_city'], data['date'], data['free_places']]
        if data['limit']:
            find_data += [data['limit']]
        rides = self.ride.get_matching_rides(*find_data)
        markup = types.InlineKeyboardMarkup()

        if len(rides) == 0:
            return {"markup": markup, "rides_text": "No rides found"}

        rides_text = ("OK, this is a list of rides. \n\n"
                      f"From - {data['from_city']}\n"
                      f"To - {data['to_city']}\n"
                      f"Date - {data['date']}\n"
                      f"Free places - {data['free_places']}")

        for ride in rides:
            if ride['user_id'] == data['id']:
                continue

            ride_button_text = (f"Price - {str(ride['price'])}֏ "
                                f" 🚙 {ride['car_color']} {ride['car_mark']} "
                                f"{str(ride['car_number']).upper().replace(" ", "")} ")
            btn = types.InlineKeyboardButton(ride_button_text, callback_data="showRide_" + str(ride['id'])
                                                                             + "_" + data['role'])
            markup.add(btn)

        markup.row(*generate(len(rides), data['role']))

        return {"markup": markup, "rides_text": rides_text}

    def ride_list(self, user_id):
        rides = self.ride.get_ride_list_by_user_id(user_id)
        markup = types.InlineKeyboardMarkup()

        if len(rides) == 0:
            return {"markup": markup, "rides_text": "You Haven't Rides yet."}

        rides_text = "OK, this is a list of rides. \n\n"

        for ride in rides:
            ride_button_text = "🔴 "

            ride_button_text += (f"Price - {str(ride['price'])}֏ "
                                 f" 🚙 {ride['car_color']} {ride['car_mark']} "
                                 f"{str(ride['car_number']).upper().replace(" ", "")} ")
            btn = types.InlineKeyboardButton(ride_button_text, callback_data="showRideDriver_" + str(ride['id'])
                                                                             + "_" + "driver")
            markup.add(btn)

        markup.row(*generate(len(rides), 'driver'))

        return {"markup": markup, "rides_text": rides_text}

    def cancel_ride_by_id(self, message, bot, ride_id):
        rides = self.ride.get_ride_for_cancel(ride_id)
        if rides is None:
            self.ride.delete_ride_by_id(ride_id)
        else:
            for ride in rides:
                print(ride)
                data = self.find_ride({"from_city": ride['from_city'], "to_city": ride['to_city'],
                                       "date": ride['ride_date'], "free_places": ride['free_places'],
                                       "id": ride['user_id'], "role": "passenger", "limit": 5})
                if data is None:

                    bot.send_message(ride['passenger_id'],
                                     text=(
                                         f"Your ride  from {ride['from_city']} to {ride['to_city']} at {ride['ride_date']}"
                                         f" was canceled, but now we can`t find another rides like this \n\n"))
                else:
                    bot.send_message(ride['passenger_id'],
                                     text=(
                                         f"Your ride  from {ride['from_city']} to {ride['to_city']} at {ride['ride_date']}"
                                         f" was canceled, we suggest you another rides like this \n\n"),
                                     reply_markup=data['markup'])

        self.ride.delete_ride_by_id(ride_id)
        bot.send_message(message.chat.id,
                         text="Your ride successfully cancelled.")
