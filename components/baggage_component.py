from telebot import types


def generate_baggage_buttons():
    markup = types.InlineKeyboardMarkup()

    markup.row(
        types.InlineKeyboardButton("Yes", callback_data="baggage_yes"),
        types.InlineKeyboardButton("No", callback_data="baggage_no"))

    return markup
