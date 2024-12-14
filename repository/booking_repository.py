from datetime import datetime
from telebot import types
from configs.storage import price, time, car, start, finish, date, passenger, to_cancel, to_back


class BookingRepository:

    def __init__(self, bot):
        self.bookings = None
        self.bot = bot

    def book_ride(self, bookings):
        self.bookings = bookings
        self.bookings.book_the_ride()
        return {'text': 'Booking successful'}

    def get_books_list(self, model):
        self.bookings = model
        books = self.bookings.get_list()['data']
        print(books)
        markup = types.InlineKeyboardMarkup()

        if len(books) == 0:
            return {"markup": markup,
                    "rides_text": "Դուք դեռ չեք ամրագրել ուղևորություններ: \n"
                                  "Ամրագրման համար կարող եք սեղմել այստեղ /passenger"}

        rides_text = "Սա Ձեր ամրագրումների ցանկն է: \n\n"

        for book in books:
            ride_button_text = (f"{start} {str(book['ride']['from_city']['name'])} "
                                f"{date} {str(book['ride']['date'])} "
                                f"{passenger} {str(book['places'])} / "
                                f"{price} {str(book['total_price'])}")
            btn = types.InlineKeyboardButton(ride_button_text, callback_data="showBook_" + str(book['id']))
            markup.add(btn)

        return {"markup": markup, "rides_text": rides_text}

    def show_booking_details(self, model):
        self.bookings = model
        booking = self.bookings.get_book()['data']
        print(booking)
        markup = types.InlineKeyboardMarkup()
        rides_text = (f"{start} {booking['ride']['from_city']['name']} {finish} {booking['ride']['to_city']['name']}\n"
                      f"{date} {booking['ride']['date']} "
                      f"{time} {datetime.strptime(booking['ride']['time'], "%H:%M:%S").strftime("%H:%M")}\n"
                      f"{car} {booking['ride']['car']['color']} {booking['ride']['car']['model']} "
                      f"{str(booking['ride']['car']['number']).upper().replace(" ", "")}\n\n"
                      f"{passenger} {booking['places']} / {price} {str(booking['total_price'])}\n\n"
                      f"____________________\n"
                      f"driver: Nº/ {booking['ride']['user']['uuid']}\n"
                      )
        if booking['ride']['user']['username'] is not None:
            rides_text += f"username: @{booking['ride']['user']['username']}"
        else:
            rides_text += f"phone: +{booking['ride']['user']['phone']}"

        btn = types.InlineKeyboardButton(f'{to_cancel}', callback_data="cancelBook_" + str(booking['id']))
        back = types.InlineKeyboardButton(f"{to_back}", callback_data="booksList")
        markup.add(btn, back)
        return {"markup": markup, "rides_text": rides_text}

    def cancel(self, model):
        self.bookings = model
        cancel = self.bookings.cancel_booking()['data']
        if cancel:
            rides_text = "Դուք չեղարկել եք ամրագրումը"
        else:
            rides_text = "try later"
        return {"rides_text": rides_text}
