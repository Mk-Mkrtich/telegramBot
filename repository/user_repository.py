from telebot import types

from configs.storage import user_ratings, user_ratings_text
from db.models.users_model import UserModel


class UserRepository:

    def __init__(self):
        self.user = UserModel()
        self.users_data = {}

    def set_role(self, user_id, role):
        self.users_data[user_id] = {"role": role}

    def get_role(self, user_id):
        return self.users_data.get(user_id, {}).get("role", "none")


    def check_user_status(self, user_id):
        self.user.user_id = user_id
        user = self.user.find_user()
        user_rating = user['bad_rating']
        blocked = False
        print(user_rating)
        if user_rating in user_ratings:
            rating = user_ratings[user_rating]
        else:
            rating = user_ratings[3]
            user_rating = 3

        text = user_ratings_text[user_rating]
        if user_rating == 3:
            blocked = True
            text += f"{user['blocked_until']}"

        return {'text': text, "rating": rating, 'blocked': blocked}

    def check_user(self, message):
        self.user.user_id = message.from_user.id
        if self.user.find_user() is None:
            self.user.user_name = message.from_user.username or ' '
            self.user.bad_rating = 0
            self.user.blocked_until = None
            self.user.create_user()

        return self.check_user_status(message.from_user.id)
