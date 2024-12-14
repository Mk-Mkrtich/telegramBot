from controllers.base_controller import BaseController
from configs.storage import ids, cash


class PassengerController(BaseController):
    def __init__(self, bot):
        super().__init__(bot)

    def finish_ride_find(self, message, places):
        if self.check_ignore("finish_ride_find_selection_" + str(message.chat.id)):
            self.append_ignore("finish_ride_find_selection_" + str(message.chat.id))
            ids.add(message.message_id)
            self.ride.free_places = places
            self.handle_ride_find(message)

    def handle_ride_find(self, message):
        ids.add(message.message_id)
        self.clear_history(message.chat.id)
        self.ride.user_id = message.chat.id
        self.ride.action = 'passenger'
        cash[message.chat.id] = {
            'from_city_id': self.ride.from_city_id,
            'to_city_id': self.ride.to_city_id,
            'date': self.ride.date,
            'free_places': self.ride.free_places,
        }
        data = self.ride_repo.ride_list(self.ride)
        ids.add(self.bot.send_message(message.chat.id, data['rides_text'], reply_markup=data['markup']).id)

    def get_ride_list_with_params(self, message, data):
        ids.add(message.message_id)
        print(data)
        self.clear_history(message.chat.id)
        self.ride.user_id = message.chat.id
        self.ride.action = data['action']
        self.ride.from_city_id = data['from_city']
        self.ride.to_city_id = data['to_city']
        self.ride.date = data['date']
        self.ride.free_places = data['free_places']
        data = self.ride_repo.ride_list(self.ride)
        ids.add(self.bot.send_message(message.chat.id, data['rides_text'], reply_markup=data['markup']).id)
