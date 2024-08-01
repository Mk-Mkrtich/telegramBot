from telebot import types
from telebot.types import InlineKeyboardButton


def generate_time_buttons():
    markup = types.InlineKeyboardMarkup()
    row = []
    for hour in range(24):
        time_str = f"{hour:02}:00"
        row.append(InlineKeyboardButton(time_str, callback_data="fideTime_" + str(time_str)))
        if (hour + 1) % 4 == 0:
            markup.row(*row)
            row = []

    return markup