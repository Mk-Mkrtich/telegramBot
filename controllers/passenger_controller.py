from controllers.base_controller import BaseController



class PassengerController(BaseController):
    def __init__(self, bot):
        super().__init__(bot)

    def finish_ride_find(self, message, places):
        self.ride.free_places = places
        self.handle_ride_find(message, 'first')

    def handle_ride_find(self, message, action):
        self.ride_repo.find_ride(
            {'from_city': self.ride.from_city, "to_city": self.ride.to_city, "date": self.ride.date,
             "free_places": self.ride.free_places, "id": message.chat.id})

    def show_ride(self, message, id):
        self.ride_repo.show_ride(message, id)

    def book_ride(self, message, ride_id, places):
        self.book.book_ride(message, ride_id, places)
