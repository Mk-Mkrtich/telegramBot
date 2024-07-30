from telebot import types

from components.paginate_buttons_component import generate
from db.models.books_model import BooksModel
from db.models.ride_model import RideModel
from configs.storage import ids


class BookingRepository:

    def __init__(self, bot):
        self.bookings = BooksModel()
        self.ride = RideModel()
        self.bot = bot

    def book_ride(self, message, ride_id, places):
        username = message.chat.username
        if not username:
            return ids.add(self.bot.send_message(message.chat.id, "Please add userName to your account").id)
        self.bookings.ride_id = ride_id
        self.bookings.booked_places = places
        self.bookings.passenger_name = username
        self.bookings.passenger_id = message.chat.id

        ride = self.ride.find_matching_ride(ride_id)
        if ride['user_id'] == message.chat.id:
            return self.bot.send_message(message.chat.id, "You cent book your ride")
        if int(ride['free_places']) == 0:
            return self.bot.send_message(message.chat.id, "The car already fully")
        self.bookings.save_to_db()
        ride_data = self.ride.update(ride_id, (int(ride['free_places']) - int(places)))

        self.bot.send_message(message.chat.id, f"Ok, we registered your Book:\n\n"
                                               f"@{username} you booked {places} Place/s on ride by "
                                               f"{ride_data['user_name']}, now you can contact with "
                                               f"@{ride_data['user_name']}:\n\n"
                                               f"From - {ride_data['from_city']}\n"
                                               f"To - {ride_data['to_city']}\n"
                                               f"Date - {ride_data['ride_date']}\n"
                                               f"Places - {ride_data['free_places']} / {ride_data['places']}\n"
                                               f"Price - {ride_data['price']}֏\n"
                                               f"🚙 {ride_data['car_color']} {ride_data['car_mark']} "
                                               f"{str(ride_data['car_number']).upper().replace(" ", "")}")

        self.bot.send_message(ride_data['user_id'], f'Hi {ride_data['user_name']}, User {username} booked '
                                                    f'{places} Place/s on Your ride at {ride_data['ride_date']} From '
                                                    f'{ride_data['from_city']} to {ride_data['to_city']}, '
                                                    f'now you can contact with @{username}.')

    def get_books_list(self, user_id, action):
        books = self.bookings.get_books_by_user(user_id, action)
        markup = types.InlineKeyboardMarkup()

        if len(books) == 0:
            return {"markup": markup, "rides_text": "You Haven't Books yet."}

        rides_text = "OK, this is a list of books. \n\n"

        for book in books:
            ride_button_text = (f"Price - {str(book['price'])}֏ "
                                f" 🚙 {book['car_color']} {book['car_mark']} "
                                f"{str(book['car_number']).upper().replace(" ", "")} ")
            btn = types.InlineKeyboardButton(ride_button_text, callback_data="showBook_" + str(book['id']))
            markup.add(btn)

        markup.row(*generate('booksList'))

        return {"markup": markup, "rides_text": rides_text}

    def show_book(self, book_id):
        book = self.bookings.get_book(book_id)
        markup = types.InlineKeyboardMarkup()

        rides_text = (f"You booked {str(book['booked_places'])} place/s on this ride. \n\n"
                      f" 🚙 {book['car_color']} {book['car_mark']} "
                      f"{str(book['car_number']).upper().replace(" ", "")} ")
        btn = types.InlineKeyboardButton('Cancel the book', callback_data="cancelBook_" + str(book['id']))
        back = types.InlineKeyboardButton("Back to list", callback_data="booksList_first")
        markup.add(btn, back)
        return {"markup": markup, "rides_text": rides_text}

    def cancel_book(self, book_id):
        book = self.bookings.get_book(book_id)
        ride_id = book['ride_id']
        places = int(book['free_places']) + int(book['booked_places'])
        if places > book['places']:
            places = book['places']
        self.ride.update(ride_id, places)

        self.bot.send_message(book['user_id'], (f'Hi {book['user_name']}, one of Users is cancel the book, now you '
                                                f'have {book['booked_places']} more free places'))
        self.bookings.delete_book(book_id)

        rides_text = "You cancel the book"

        return {"rides_text": rides_text}
