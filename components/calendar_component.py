import calendar
from telebot import types
from datetime import datetime
from configs.storage import ids
from components.places_buttons_component import generate

class CalendarComponent:

    def __init__(self):
        self.year = datetime.now().year
        self.month = datetime.now().month

    def generate_calendar_keyboard(self):
        current_date = datetime.now()
        keyboard = types.InlineKeyboardMarkup()

        # Month and Year navigation
        keyboard.add(types.InlineKeyboardButton('<', callback_data=f'prev_month_{self.year}_{self.month}'),
                     types.InlineKeyboardButton(f'{calendar.month_name[self.month]} {self.year}', callback_data='ignore'),
                     types.InlineKeyboardButton('>', callback_data=f'next_month_{self.year}_{self.month}'))

        # Days of the week
        days_of_week = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
        keyboard.row(*[types.InlineKeyboardButton(day, callback_data='ignore') for day in days_of_week])

        # Days of the month
        month_calendar = calendar.monthcalendar(self.year, self.month)
        for week in month_calendar:
            row = []
            for day in week:
                if day == 0:
                    row.append(types.InlineKeyboardButton(' ', callback_data='ignore'))
                else:
                    if (self.year < current_date.year) or \
                            (self.year == current_date.year and self.month < current_date.month) or \
                            (self.year == current_date.year and self.month == current_date.month
                             and day < current_date.day):
                        row.append(types.InlineKeyboardButton(f'🚫{day}', callback_data='ignore'))
                    else:
                        row.append(types.InlineKeyboardButton(str(day), callback_data=f'day_{self.year}_{self.month}_{day}'))
            keyboard.row(*row)

        return keyboard

    def handle_keyboard(self, bot, callback, ride):
        data = callback.data.split('_')
        if data[0] == 'prev' and data[1] == 'month':
            year, month = int(data[2]), int(data[3])
            month -= 1
            if month == 0:
                month = 12
                year -= 1
            self.year = year
            self.month = month
            markup = self.generate_calendar_keyboard()
            return ['edit', markup]
        elif data[0] == 'next' and data[1] == 'month':
            year, month = int(data[2]), int(data[3])
            month += 1
            if month == 13:
                month = 1
                year += 1
            self.year = year
            self.month = month
            markup = self.generate_calendar_keyboard()
            return ['edit', markup]

        elif data[0] == 'day':
            year, month, day = int(data[1]), int(data[2]), int(data[3])
            ride.date = f"{year}-{month:02}-{day:02}"
            ids.add(bot.send_message(callback.message.chat.id, f"Selected date: {ride.date}").id)

            return ['send', generate()]

