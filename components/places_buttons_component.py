from telebot import types


def generate():
    markup = types.InlineKeyboardMarkup()
    passengers_count = []
    for i in range(1, 7):
        btn = types.InlineKeyboardButton(i, callback_data="passengersCount_" + str(i))
        passengers_count.append(btn)

    markup.row(*passengers_count)

    return markup
