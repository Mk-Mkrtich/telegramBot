from admin.api_call import admin_call


class CitiesModel:

    def get_cities(self):
        try:
            cities = admin_call(None, "tcities")['data']['cities']
        except Exception as e:
            print(str(e), e.__context__, e.__class__)
        else:
            return cities

