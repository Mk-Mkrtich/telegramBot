from telebot import types


def generate_start_buttons(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("I don't know what it is", callback_data='help'))
    btn1 = types.InlineKeyboardButton("Create a Ride", callback_data='driver')
    btn2 = types.InlineKeyboardButton("Find a Ride", callback_data='passenger')
    btn3 = types.InlineKeyboardButton("My Rides List", callback_data='ridesList_' + str(message.chat.id))
    btn4 = types.InlineKeyboardButton("Find Books List", callback_data='booksList_' + str(message.chat.id))
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)

    return markup
