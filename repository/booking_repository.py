from telebot import types

from components.paginate_buttons_component import generate
from db.models.books_model import BooksModel
from db.models.ride_model import RideModel
from repository.user_repository import UserRepository
from configs.storage import ids, start, finish, date, time, passenger, price, car, to_back, to_cancel


class BookingRepository:

    def __init__(self, bot):
        self.bookings = BooksModel()
        self.ride = RideModel()
        self.bot = bot
        self.user_repository = UserRepository()

    def book_ride(self, message, ride_id, places):
        username = message.chat.username
        self.bookings.ride_id = ride_id
        self.bookings.booked_places = places
        self.bookings.passenger_name = username
        self.bookings.passenger_id = message.chat.id

        ride = self.ride.find_matching_ride(ride_id)
        if ride['user_id'] == message.chat.id:
            return self.bot.send_message(message.chat.id, "Դուք չեք կարող ամրագրել ձեր ուղևորությունը")
        if int(ride['free_places']) == 0:
            return self.bot.send_message(message.chat.id, "Բոլոր տեղերն արդեն ամրագրված են")
        self.bookings.save_to_db()
        ride_data = self.ride.update(ride_id, (int(ride['free_places']) - int(places)))

        self.bot.send_message(message.chat.id, f"Մենք գրանցում ենք ձեր ամրագրումը.\n\n"
                                               f"@{username} Դուք ամրագրել եք {places} տեղ "
                                               f"{ride_data['user_name']}, այժմ կարող եք կապ հաստատել "
                                               f"@{ride_data['user_name']} -ի հետ:\n\n"
                                               f"ID: {ride_data['user_id']} \nսա վարորդի ID-ն է, այն ձեզ անհրաժեշտ "
                                               f"կլինի բողոքների համար:\n\n"
                                               f"{start} {ride_data['from_city']} "
                                               f"{finish} {ride_data['to_city']}\n"
                                               f"{date} {ride_data['ride_date']} "
                                               f"{time} {ride_data['ride_time']}\n"
                                               f"{passenger} {ride_data['free_places']} / {ride_data['places']} "
                                               f"{price} {ride_data['price']}\n"
                                               f"{car} {ride_data['car_color']} {ride_data['car_mark']} "
                                               f"{str(ride_data['car_number']).upper().replace(" ", "")}\n\n"
                                               f"Խնդրում եմ, հիշեք, որ գործ ունեք իրական մարդկանց հետ, "
                                               f"խնդրում եմ մի ուշացեք, չեղարկեք ուղևորությունից 2 ժամ առաջ։ \n\n"
                                               f"Եթե նկատում եք ուղևորների անընդունելի վարքագիծը,"
                                               f" տեղեկացրեք մեզ:"
                                               f"Գրեք հաղորդագրություն բոտին՝ /support նշելով ուղևորի ID"
                                               f" և բողոքի պատճառ")

        user = self.user_repository.check_user_status(message.chat.id)
        self.bot.send_message(ride_data['user_id'], f'Ողջույն {ride_data['user_name']}, {username}-ը ամրագրեց '
                                                    f'{places} տեղ {ride_data['ride_date']} '
                                                    f'{ride_data['ride_time']}-ին \n'
                                                    f'{ride_data['from_city']}-ից {ride_data['to_city']}, '
                                                    f'այժմ կարող եք կապ հաստատել @{username} -ի հետ. '
                                                    f"ID: {message.chat.id} \nսա ուղևորի ID-ն է, այն ձեզ անհրաժեշտ "
                                                    f"կլինի բողոքների համար:\n\n"
                                                    f"{user['text']} Ուղևորի վարկանիշ \n\n"
                              )

    def get_books_list(self, user_id, action):
        books = self.bookings.get_books_by_user(user_id, action)
        markup = types.InlineKeyboardMarkup()

        if len(books) == 0:
            return {"markup": markup,
                    "rides_text": "Դուք դեռ չեք ամրագրել ուղևորություններ: \n"
                                  "Ամրագրման համար կարող եք սեղմել այստեղ /passenger"}

        rides_text = "Սա Ձեր ամրագրումների ցանկն է: \n\n"

        for book in books:
            ride_button_text = (f"{price} {str(book['price'])} "
                                f"{time} {str(book['ride_time'])} "
                                f"{car} {book['car_color']} {book['car_mark']} ")
            btn = types.InlineKeyboardButton(ride_button_text, callback_data="showBook_" + str(book['id']))
            markup.add(btn)

        markup.row(*generate('booksList'))

        return {"markup": markup, "rides_text": rides_text}

    def show_book(self, book_id):
        book = self.bookings.get_book(book_id)
        markup = types.InlineKeyboardMarkup()
        user = self.user_repository.check_user_status(book['user_id'])

        rides_text = (f"Դուք ամրագրել եք {str(book['booked_places'])} տեղ \n\n"
                      f"{start} {book['from_city']} "
                      f"{finish} {book['to_city']}\n"
                      f"{price} {book['price']} դրամ, ընդ. {book['booked_places'] * book['price']} դրամ\n"
                      f"{date} {book['ride_date']} "
                      f"{time} {book['ride_time']}\n"
                      f"{car} {book['car_color']} {book['car_mark']} "
                      f"{str(book['car_number']).upper().replace(" ", "")}\n"
                      f"{passenger} @{book['user_name']} "
                      f"ID: {book['user_id']}\n"
                      f"{user['text']} Վարորդի վարկանիշ \n\n"
                      )
        btn = types.InlineKeyboardButton(f'{to_cancel}', callback_data="cancelBook_" + str(book['id']))
        back = types.InlineKeyboardButton(f"{to_back}", callback_data="booksList_first")
        markup.add(btn, back)
        return {"markup": markup, "rides_text": rides_text}

    def cancel_book(self, book_id):
        book = self.bookings.get_book(book_id)
        ride_id = book['ride_id']
        places = int(book['free_places']) + int(book['booked_places'])
        if places > book['places']:
            places = book['places']
        self.ride.update(ride_id, places)

        self.bot.send_message(book['user_id'], (
            f'Ողջույն {book['user_name']}, ուղևորներից մեկը չեղարկել է ամրագրումը\n\n'
            f' {book['from_city']}ից {book['to_city']}\n'
            f' {date} {book['ride_date']} {time} {book['ride_time']} \n\n'
            f"այժմ դուք ունեք ևս {book['booked_places']} ազատ տեղ"))
        self.bookings.delete_book(book_id)

        rides_text = "Դուք չեղարկել եք ամրագրումը"

        return {"rides_text": rides_text}
