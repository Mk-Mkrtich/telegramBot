from telebot import types
from telebot.types import InlineKeyboardButton
from configs.storage import can_not
import datetime


def generate_time_buttons():
    current_time = datetime.datetime.now().hour
    markup = types.InlineKeyboardMarkup()
    row = []
    for hour in range(24):
        time_str = f"{hour:02}:00"
        callback_data = ""
        if hour > current_time:
            callback_data += "fideTime_" + str(time_str)
            text = time_str
        else:
            callback_data += "ignore"
            text = can_not + " " + time_str
        row.append(InlineKeyboardButton(text, callback_data=callback_data))
        if (hour + 1) % 4 == 0:
            markup.row(*row)
            row = []

    return markup