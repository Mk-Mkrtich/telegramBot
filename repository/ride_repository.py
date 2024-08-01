from telebot import types

from components.paginate_buttons_component import generate
from db.models.ride_model import RideModel
from configs.storage import start, finish, date, time, passenger, price, car, to_back, to_cancel


class RideRepository:

    def __init__(self, bot):
        self.ride = RideModel()
        self.bot = bot

    def show_ride(self, id, role, suggest=None):
        ride = self.ride.find_matching_ride(id)
        markup = types.InlineKeyboardMarkup()

        if ride is None:
            return {"markup": markup, "rides_text": "Ride not found."}

        rides_text = (f"{start} {ride['from_city']} "
                      f"{finish} {ride['to_city']}\n"
                      f"{date} {ride['ride_date']} "
                      f"{time} {ride['ride_time']}\n"
                      f"{passenger} {ride['free_places']} / {ride['places']} "
                      f"{price} {ride['price']}֏\n"
                      f"{car} {ride['car_color']} {ride['car_mark']} "
                      f"{str(ride['car_number']).upper().replace(" ", "")}\n\n"
                      )

        if role == "passenger":
            rides_text += f"Select places count for BOOKING"
            places_count = []
            for i in range(1, int(ride['free_places']) + 1):
                btn = types.InlineKeyboardButton(f"{passenger}" + str(i),
                                                 callback_data="bookRide_" + str(ride['id']) + "_" + str(i))
                places_count.append(btn)

            markup.row(*places_count)
            back = types.InlineKeyboardButton(f"{to_back}", callback_data="ridesForPassenger_first")
        else:
            back = types.InlineKeyboardButton(f"{to_back}", callback_data="ridesForDriver_first")
            cancel = types.InlineKeyboardButton(f"{to_cancel}", callback_data="cancelRide_" + str(id))
            markup.add(cancel)
        if suggest is None:
            markup.add(back)
        return {"markup": markup, "rides_text": rides_text}

    def find_ride(self, data, action, paginate=None, suggest=None):
        find_data = [data['from_city'], data['to_city'], data['date'], data['free_places']]

        rides = self.ride.get_matching_rides(*find_data, data['id'], action)
        markup = types.InlineKeyboardMarkup()

        if len(rides) == 0:
            return {"markup": markup, "rides_text": "No rides found"}

        if suggest is None:
            rides_text = "OK, this is a list of rides. \n\n"

        else:
            rides_text = "We suggest you another rides. \n\n"

        rides_text += (f"{start} {data['from_city']} "
                       f"{finish} {data['to_city']}\n"
                       f"{date} {data['date']}\n"
                       f"{passenger} {data['free_places']}")
        for ride in rides:
            callback_params = "showRideForPassenger_" + str(ride['id'])
            if suggest is not None:
                callback_params += "_suggest"
            else:
                callback_params += "_"
            ride_button_text = (f"{price} {str(ride['price'])} "
                                f"{time} {str(ride['ride_time'])} "
                                f"{car} {ride['car_color']} {ride['car_mark']} "
                                f"{str(ride['car_number']).upper().replace(" ", "")} ")
            btn = types.InlineKeyboardButton(ride_button_text, callback_data=callback_params)
            markup.add(btn)

        if paginate is None:
            markup.row(*generate(data['type']))

        return {"markup": markup, "rides_text": rides_text, "count": len(rides)}

    def ride_list(self, user_id, action):
        rides = self.ride.get_ride_list_by_user_id(user_id, action)
        markup = types.InlineKeyboardMarkup()

        if len(rides) == 0:
            return {"markup": markup, "rides_text": "You Haven't Rides yet."}

        rides_text = "OK, this is a list of rides. \n\n"

        for ride in rides:
            ride_button_text = (f"{price} {str(ride['price'])} {date} {str(ride['ride_date'])} {time} {str(ride['ride_time'])}"
                                f" {car} {str(ride['car_number']).upper().replace(" ", "")} ")
            btn = types.InlineKeyboardButton(ride_button_text, callback_data="showRideForDriver_" + str(ride['id'])
                                                                             + "_" + "driver")
            markup.add(btn)

        markup.row(*generate('ridesForDriver'))

        return {"markup": markup, "rides_text": rides_text}

    def cancel_ride_by_id(self, message, bot, ride_id):
        rides = self.ride.get_ride_for_cancel(ride_id)
        if rides is None:
            self.ride.delete_ride_by_id(ride_id)
        else:
            for ride in rides:
                data = self.find_ride({"from_city": ride['from_city'], "to_city": ride['to_city'],
                                       "date": ride['ride_date'], "free_places": ride['free_places'],
                                       "id": ride['user_id'], "type": "ridesForPassenger"}, "first", "no_need",
                                      'suggest')
                if data['count'] == 0:

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
