from db.models.books_model import BooksModel
from db.models.ride_model import RideModel
from components.start_buttons_component import generate_start_buttons


class BookingRepository:

    def __init__(self, bot):
        self.bookings = BooksModel()
        self.ride = RideModel()
        self.bot = bot

    def book_ride(self, message, ride_id, places):
        username = message.chat.username
        if not username:
            return self.bot.send_message(message.chat.id, "Please add userName to your account")
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

        markup = generate_start_buttons(message)
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
                                               f"{str(ride_data['car_number']).upper().replace(" ", "")}",
                              reply_markup=markup)

        self.bot.send_message(ride_data['user_id'], f'Hi {ride_data['user_name']}, User {username} booked '
                                                    f'{places} Place/s on Your ride at {ride_data['ride_date']} From '
                                                    f'{ride_data['from_city']} to {ride_data['to_city']}, '
                                                    f'now you can contact with @{username}.')





