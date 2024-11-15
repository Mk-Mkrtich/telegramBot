from telebot import types
from configs.storage import colors


def generate_cars_buttons(data):
    markup = types.InlineKeyboardMarkup()
    for i in data:
        print(i)
        text = f"{colors[i['color']]}  {i['model']} N: {i['number']}"
        btn = types.InlineKeyboardButton(text, callback_data=f"userCar_{str(i['id'])}_{str(i['user_id'])}")
        markup.add(btn)

    btn = types.InlineKeyboardButton('Create New Car', callback_data=f"userNewCar_{str(data[0]['user_id'])}")
    markup.add(btn)
    return markup
