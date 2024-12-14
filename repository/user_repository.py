from admin.api_call import admin_call


class UserRepository:

    def __init__(self):
        self.users_data = {}

    def set_role(self, user_id, role):
        self.users_data[user_id] = {"role": role}

    def get_role(self, user_id):
        return self.users_data.get(user_id, {}).get("role", "none")

    def check_user(self, message):
        phone_number = None
        if message.contact is not None:
            phone_number = message.contact.phone_number
        user = admin_call({
            'tuid': message.from_user.id,
            'username': message.from_user.username or None,
            'phone': phone_number
        }, "tuser/get", 'POST')
        if user['code'] == 200:
            if user is None or user['data']['is_active'] is False:
                return {'ok': False, 'message': 'inactive'}
            return {'ok': True, 'message': 'good'}
        elif user['code'] == 401:
            return {'ok': False, 'message': 'contact'}
        else:
            return {'ok': False, 'message': 'error'}
