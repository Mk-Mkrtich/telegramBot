import calendar
from telebot import types

def generate_calendar_keyboard(year, month):
    keyboard = types.InlineKeyboardMarkup()

    # Month and Year navigation
    keyboard.add(types.InlineKeyboardButton('<', callback_data=f'prev_month_{year}_{month}'),
                 types.InlineKeyboardButton(f'{calendar.month_name[month]} {year}', callback_data='ignore'),
                 types.InlineKeyboardButton('>', callback_data=f'next_month_{year}_{month}'))

    # Days of the week
    days_of_week = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
    keyboard.row(*[types.InlineKeyboardButton(day, callback_data='ignore') for day in days_of_week])

    # Days of the month
    month_calendar = calendar.monthcalendar(year, month)
    for week in month_calendar:
        row = []
        for day in week:
            if day == 0:
                row.append(types.InlineKeyboardButton(' ', callback_data='ignore'))
            else:
                row.append(types.InlineKeyboardButton(str(day), callback_data=f'day_{year}_{month}_{day}'))
        keyboard.row(*row)

    return keyboard
