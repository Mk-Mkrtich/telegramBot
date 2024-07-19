from components.calendar_component import CalendarComponent


class CommonRepository:

    def __init__(self, bot):
        self.bot = bot
        self.calendar = CalendarComponent()

    def handle_calendar(self, callback):
        data = callback.data.split('_')
        year, month = int(data[2]), int(data[3])

        if data[0] == 'prev':
            month -= 1
            if month == 0:
                month = 12
                year -= 1
        elif data[0] == 'next':
            month += 1
            if month == 13:
                month = 1
                year += 1

        self.calendar.year = year
        self.calendar.month = month
        markup = self.calendar.generate_calendar_keyboard()
        self.bot.edit_message_text("Please select a date:", callback.message.chat.id, callback.message.message_id,
                                   reply_markup=markup)
