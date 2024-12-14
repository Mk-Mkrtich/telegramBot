from controllers.base_controller import BaseController
from configs.storage import ids


class RideController(BaseController):
    def __init__(self, bot):
        super().__init__(bot)

    def get_ride_list(self, message, action):
        self.ride.user_id = message.chat.id
        self.ride.action = action
        data = self.ride_repo.ride_list(self.ride)
        self.clear_history(message.chat.id)
        self.trash_ignore(message.chat.id)
        ids.add(self.bot.send_message(message.chat.id, data['rides_text'], reply_markup=data['markup']).id)

    def suggest_ride_list(self, message, data):
        self.ride.from_city_id = data['from_city_id']
        self.ride.to_city_id = data['to_city_id']
        self.ride.date = data['date']
        self.ride.free_places = data['free_places']
        self.get_ride_list(message, 'passenger')

    def show_ride(self, message, ride_id, action):
        ids.add(message.message_id)
        self.ride.action = action
        self.ride.id = ride_id
        data = self.ride_repo.show_ride(self.ride)
        ids.add(self.bot.send_message(message.chat.id, data['rides_text'], reply_markup=data['markup']).id)

    def cancel_ride(self, message, ride_id):
        self.ride.id = ride_id
        data = self.ride_repo.cancel_ride_by_id(self.ride)
        self.bot.send_message(message.chat.id, data['rides_text'], reply_markup=data['markup'])
        self.get_ride_list(message, 'driver')
