from telebot import types
from telebot.types import InlineKeyboardButton
from configs.storage import can_not, times
import datetime


def generate_time_buttons(date):
    current_time = datetime.datetime.now().hour
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    date = str(date).split('-')

    markup = types.InlineKeyboardMarkup()
    row = []
    for hour in range(24):
        time_str = f"{hour:02}:00"
        callback_data = ""
        cant = None
        if year == int(date[0]) and month == int(date[1]) and day == int(date[2]) and hour <= current_time:
            callback_data += "ignore"
            cant = can_not
        else:
            callback_data += "fideTime_" + str(time_str)

        row.append(InlineKeyboardButton(f"{cant or times[time_str]}{time_str}", callback_data=callback_data))
        if (hour + 1) % 4 == 0:
            markup.row(*row)
            row = []

    return markup