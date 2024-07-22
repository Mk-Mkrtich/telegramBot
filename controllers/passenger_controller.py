from controllers.base_controller import BaseController


class PassengerController(BaseController):
    def __init__(self, bot):
        super().__init__(bot)

    def finish_ride_find(self, message, places):
        if self.check_ignore("finish_ride_find_selection"):
            self.append_ignore("finish_ride_find_selection")
            self.ride.free_places = places
            self.handle_ride_find(message, 'first')

    def handle_ride_find(self, message, action):
        self.end_message_id = message.message_id
        self.clear_history(message.chat.id)
        data = self.ride_repo.find_ride(
            {'from_city': self.ride.from_city, "to_city": self.ride.to_city, "date": self.ride.date,
             "free_places": self.ride.free_places, "id": message.chat.id})
        self.bot.send_message(message.chat.id, data['rides_text'], reply_markup=data['markup'])
        self.start_message_id = message.message_id

    def show_ride(self, message, id):
        data = self.ride_repo.show_ride(message, id)
        self.bot.send_message(message.chat.id, data['rides_text'], reply_markup=data['markup'])

    def book_ride(self, message, ride_id, places):
        self.end_message_id = message.message_id
        self.clear_history(message.chat.id)
        self.book.book_ride(message, ride_id, places)
