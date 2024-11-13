from admin.api_call import admin_call


class CarModel:

    def __init__(self):
        self.model = '',
        self.color = '',
        self.number = '',
        self.tuid = ''

    def check_car(self):
        print(self.__dict__)
        new_car_data = admin_call(self.__dict__, "tuser/cars/create", 'POST')
        return new_car_data
