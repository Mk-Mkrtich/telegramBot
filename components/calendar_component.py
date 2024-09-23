import calendar
from telebot import types
from datetime import datetime

from components.time_component import generate_time_buttons
from configs.storage import ids, can_not, time, passenger, months
from components.places_buttons_component import generate

class CalendarComponent:

    def __init__(self):
        self.year = datetime.now().year
        self.month = datetime.now().month

    def generate_calendar_keyboard(self):
        current_date = datetime.now()
        keyboard = types.InlineKeyboardMarkup()

        # Month and Year navigation
        keyboard.row(types.InlineKeyboardButton('<', callback_data=f'prev_month_{self.year}_{self.month}'),
                     types.InlineKeyboardButton(f'{months[calendar.month_name[self.month]]}', callback_data='ignore'),
                     types.InlineKeyboardButton(f'{self.year}', callback_data='ignore'),
                     types.InlineKeyboardButton('>', callback_data=f'next_month_{self.year}_{self.month}'))

        # Days of the week
        days_of_week = ['Երկ', 'Երք', 'Չոր', 'Հինգ', 'Ուր', 'Շաբ', 'Կի']
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
                        row.append(types.InlineKeyboardButton(f'{can_not}{day}', callback_data='ignore'))
                    else:
                        row.append(types.InlineKeyboardButton(str(day), callback_data=f'day_{self.year}_{self.month}_{day}'))
            keyboard.row(*row)

        return keyboard

    def handle_keyboard(self, bot, callback, ride, role):
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
            ids.add(bot.send_message(callback.message.chat.id, f"Ընտրված ամսաթիվ: {ride.date}").id)
            if role == 'driver':
                next_step_data = generate_time_buttons(ride.date)
                next_step_text = f"Խնդրում ենք ընտրել ժամը {time}."
            else:
                next_step_data = generate()
                next_step_text = f"Խնդրում ենք ընտրել ազատ տեղերի քանակը {passenger}."

            return ['send', next_step_data, next_step_text]

