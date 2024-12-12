from datetime import datetime

from telebot import types

from db.models.ride_model import RideModel
from repository.user_repository import UserRepository
from configs.storage import start, finish, date, time, passenger, price, car, to_back, to_cancel, cash


class RideRepository:

    def __init__(self, bot):
        self.ride = None
        self.bot = bot
        self.user_repository = UserRepository()

    def show_ride(self, ride_model):
        self.ride = ride_model

        ride = self.ride.get_ride_by_id()['data']
        markup = types.InlineKeyboardMarkup()

        if ride is None:
            return {"markup": markup, "rides_text": "Ուղևորություններ չեն գտնվել"}

        rides_text = ''
        if self.ride.action == 'driver':
            rides_text += (f"Ride ID: {str(ride['id'])}\n"
                           f"Yours ID: {str(ride['user']['uuid'])}\n")

        rides_text += (f"{start} {ride['from_city']['name']} "
                       f"{finish} {ride['to_city']['name']}\n"
                       f"{date} {ride['date']} "
                       f"{time} {datetime.strptime(ride['time'], "%H:%M:%S").strftime("%H:%M")}\n"
                       f"{passenger} {ride['free_places']} / {ride['places']} "
                       f"{price} {ride['price']}֏\n"
                       f"{car} {ride['car']['color']} {ride['car']['model']} "
                       f"{str(ride['car']['number']).upper().replace(" ", "")}\n"
                       )

        if self.ride.action == 'driver':
            rides_text += (f"\n_____________________\n\n"
                           f"Bookings List\n")
            for booking in ride['bookings']:
                rides_text += (
                    f"____________________\n"
                    f"user: Nº/ {booking['passenger_id']}\n"
                    f"user name: @{booking['passenger_username']}\n"
                    f"{passenger} {booking['places']} / {price} {booking['total_price']}\n")

            cancel = types.InlineKeyboardButton(f"{to_cancel}", callback_data="cancelRide_" + str(ride['id']))
            back = types.InlineKeyboardButton(f"{to_back}", callback_data="rideList_" + self.ride.action)
            markup.add(cancel)

        else:
            rides_text += (f"\n\nvarordi varkanish {ride['user']['rating']['rating']}\n"
                           f"chexarkumneri qanak {ride['user']['history']['cancelled']}\n"
                           f"uxevorutyunneri qanak {ride['user']['history']['rides']}\n"
                           f"boxoqneri qanak {ride['user']['rating']['scumbags']}\n\n"
                           f"Ընտրեք տեղերի քանակը ամրագրման համար")
            places_count = []
            for i in range(1, int(ride['free_places']) + 1):
                btn = types.InlineKeyboardButton(f"{passenger}" + str(i),
                                                 callback_data="bookRide_" + str(ride['id']) + "_" + str(i))
                places_count.append(btn)

            markup.row(*places_count)
            print(self.ride.__dict__, "this is a ride data before request to admin")
            back = types.InlineKeyboardButton(f"{to_back}", callback_data=("rideList_" + self.ride.action))

        markup.add(back)
        return {"markup": markup, "rides_text": rides_text}

    # def find_ride(self, data, action, paginate=None, suggest=None):
    #     find_data = [data['from_city'], data['to_city'], data['date'], data['free_places']]
    #
    #     rides = self.ride.get_matching_rides(*find_data, data['id'], action)
    #     markup = types.InlineKeyboardMarkup()
    #
    #     if len(rides) == 0:
    #         return {"markup": markup, "rides_text": "Ուղևորություններ չեն գտնվել"}
    #
    #     if suggest is None:
    #         rides_text = "Սա ուղևորությունների ցանկն է: \n\n"
    #
    #     else:
    #         rides_text = "Առաջարկում ենք ձեզ նման այլ ուղևորություններ \n\n"
    #
    #     rides_text += (f"{start} {data['from_city']} "
    #                    f"{finish} {data['to_city']}\n"
    #                    f"{date} {data['date']}\n"
    #                    f"{passenger} {data['free_places']}")
    #     for ride in rides:
    #         user = self.user_repository.check_user_status(ride['user_id'])
    #         callback_params = "showRideForPassenger_" + str(ride['id'])
    #         if suggest is not None:
    #             callback_params += "_suggest"
    #         else:
    #             callback_params += "_"
    #
    #         ride_button_text = (
    #                             f"{user['rating']} "
    #                             f"{price} {str(ride['price'])} "
    #                             f"{time} {str(ride['ride_time'])} "
    #                             f"{car} {ride['car_color']} {ride['car_mark']} ")
    #         btn = types.InlineKeyboardButton(ride_button_text, callback_data=callback_params)
    #         markup.add(btn)
    #
    #     if paginate is None:
    #         markup.row(*generate(data['type']))
    #
    #     return {"markup": markup, "rides_text": rides_text, "count": len(rides)}

    def ride_list(self, ride):
        self.ride = ride
        print(ride.__dict__)
        print(cash)
        if self.ride.action == 'passenger':
            self.ride.from_city_id = self.ride.from_city_id or cash[self.ride.user_id]['from_city_id']
            self.ride.to_city_id = self.ride.to_city_id or cash[self.ride.user_id]['to_city_id']
            self.ride.date = self.ride.date or cash[self.ride.user_id]['date']
            self.ride.free_places = self.ride.free_places or cash[self.ride.user_id]['free_places']

        rides = self.ride.get_ride_list()['data']
        markup = types.InlineKeyboardMarkup()

        if len(rides) == 0:
            return {"markup": markup,
                    "rides_text": "uxevorutyunner chkan"}

        for ride in rides:
            if self.ride.action == 'driver':

                ride_button_text = (f" {start} {ride['from_city']['name']} "
                                    f" {finish} {str(ride['to_city']['name'])} "
                                    f" {date} {str(ride['date'])} "
                                    f" {datetime.strptime(str(ride['time']), "%H:%M:%S").strftime("%H:%M")}"
                                    f"{passenger} {str(ride['free_places'])}/{str(ride['places'])}"
                                    )
            else:
                ride_button_text = (f"{price} {ride['car']['color']} {ride['car']['model']}"
                                    f" {time} {datetime.strptime(ride['time'], "%H:%M:%S").strftime("%H:%M")}"
                                    f"{passenger} {str(ride['free_places'])}/{str(ride['places'])} "
                                    )

            btn = types.InlineKeyboardButton(ride_button_text, callback_data="showRide_" + str(ride['id'])
                                                                             + "_" + self.ride.action)
            markup.add(btn)

        return {"markup": markup, "rides_text": 'list'}

    def cancel_ride_by_id(self, ride):
        self.ride = ride
        canceled_ride = self.ride.cancel_ride()['data']
        if canceled_ride['status']:
            markup = types.InlineKeyboardMarkup()
            return {"markup": markup, "rides_text": canceled_ride['text'] + '\n\n duq karox es stexcel@ nor -> /driver'}
