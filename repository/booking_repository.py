class BookingRepository:

    def __init__(self, bot):
        self.bookings = None
        self.bot = bot

    def book_ride(self, bookings):
        self.bookings = bookings
        self.bookings.book_the_ride()
        return {'text': 'Booking successful'}

    # def get_books_list(self, user_id, action):
    #     books = self.bookings.get_books_by_user(user_id, action)
    #     markup = types.InlineKeyboardMarkup()
    #
    #     if len(books) == 0:
    #         return {"markup": markup,
    #                 "rides_text": "Դուք դեռ չեք ամրագրել ուղևորություններ: \n"
    #                               "Ամրագրման համար կարող եք սեղմել այստեղ /passenger"}
    #
    #     rides_text = "Սա Ձեր ամրագրումների ցանկն է: \n\n"
    #
    #     for book in books:
    #         ride_button_text = (f"{price} {str(book['price'])} "
    #                             f"{time} {str(book['ride_time'])} "
    #                             f"{car} {book['car_color']} {book['car_mark']} ")
    #         btn = types.InlineKeyboardButton(ride_button_text, callback_data="showBook_" + str(book['id']))
    #         markup.add(btn)
    #
    #     markup.row(*generate('booksList'))
    #
    #     return {"markup": markup, "rides_text": rides_text}
    #
    # def show_book(self, book_id):
    #     book = self.bookings.get_book(book_id)
    #     markup = types.InlineKeyboardMarkup()
    #     user = self.user_repository.check_user_status(book['user_id'])
    #
    #     rides_text = (f"Դուք ամրագրել եք {str(book['booked_places'])} տեղ \n\n"
    #                   f"{start} {book['from_city']} "
    #                   f"{finish} {book['to_city']}\n"
    #                   f"{price} {book['price']} դրամ, ընդ. {book['booked_places'] * book['price']} դրամ\n"
    #                   f"{date} {book['ride_date']} "
    #                   f"{time} {book['ride_time']}\n"
    #                   f"{car} {book['car_color']} {book['car_mark']} "
    #                   f"{str(book['car_number']).upper().replace(" ", "")}\n"
    #                   f"{passenger} @{book['user_name']} "
    #                   f"ID: {book['user_id']}\n"
    #                   f"{user['text']} Վարորդի վարկանիշ \n\n"
    #                   )
    #     btn = types.InlineKeyboardButton(f'{to_cancel}', callback_data="cancelBook_" + str(book['id']))
    #     back = types.InlineKeyboardButton(f"{to_back}", callback_data="booksList_first")
    #     markup.add(btn, back)
    #     return {"markup": markup, "rides_text": rides_text}
    #
    # def cancel_book(self, book_id):
    #     book = self.bookings.get_book(book_id)
    #     ride_id = book['ride_id']
    #     places = int(book['free_places']) + int(book['booked_places'])
    #     if places > book['places']:
    #         places = book['places']
    #     self.ride.update(ride_id, places)
    #
    #     self.bot.send_message(book['user_id'], (
    #         f'Ողջույն {book['user_name']}, ուղևորներից մեկը չեղարկել է ամրագրումը\n\n'
    #         f' {book['from_city']}ից {book['to_city']}\n'
    #         f' {date} {book['ride_date']} {time} {book['ride_time']} \n\n'
    #         f"այժմ դուք ունեք ևս {book['booked_places']} ազատ տեղ"))
    #     self.bookings.delete_book(book_id)
    #
    #     rides_text = "Դուք չեղարկել եք ամրագրումը"
    #
    #     return {"rides_text": rides_text}
