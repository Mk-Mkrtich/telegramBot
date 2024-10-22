from admin.api_call import admin_call


class UserRepository:

    def __init__(self):
        self.users_data = {}

    def set_role(self, user_id, role):
        self.users_data[user_id] = {"role": role}

    def get_role(self, user_id):
        return self.users_data.get(user_id, {}).get("role", "none")

    def check_user(self, message):
        user = admin_call({'tuid': message.from_user.id, 'username': message.from_user.username or None}, "tuser/get", 'POST')
        print(user)
        if user['code'] == 200:
            if user is None or user['data']['is_active'] is False:
                return False
            return True
        else:
            print(user)
            return False
