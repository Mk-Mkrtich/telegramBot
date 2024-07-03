import telebot
from telebot import types
import calendar
import datetime

bot = telebot.TeleBot('7281065108:AAG2mnguDewytqYRsTtR24SZ0-L8jBkCyA4')

from_city_var = ''
to_city_var = ''
ride_date = ''
places = ''
price = ''
car_mark = ''
car_number = ''
car_color = ''

find_from_city = ''
find_to_city = ''
find_date = ''
find_places = ''

cities = [
    "gyumri",
    "erevan",
    "vanadzor",
    "kirovakan",
    "caxkadzor",
    "hrazdan"
]


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

@bot.message_handler(commands=['start'])
def main(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("I don't know what it is", callback_data='help'))
    btn1 = types.InlineKeyboardButton("I am a Driver", callback_data='driver')
    btn2 = types.InlineKeyboardButton("I am a Passenger", callback_data='passenger')
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id, "Hello " + message.from_user.first_name +
                     ", I am your online friend. I will help you to find and create your ride. "
                     "Let me know, how you want to use the bot: as driver or as passenger?", reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback(callback):
    global from_city_var, to_city_var
    data = callback.data.split('_')

    if data[0] == 'help':
        bot.send_message(callback.message.chat.id, "You can find a ride on the way you need, "
                                                   "also you can share your rides with other users.")

    elif data[0] == 'driver':
        chunk = chunk_array(cities)
        markup = types.InlineKeyboardMarkup()
        for i in range(len(chunk)):
            btn1 = types.InlineKeyboardButton(chunk[i][0], callback_data=chunk[i][0])
            cit1 = [btn1]
            if len(chunk[i]) > 1:
                btn2 = types.InlineKeyboardButton(chunk[i][1], callback_data=chunk[i][1])
                cit1.append(btn2)
                if len(chunk[i]) > 2:
                    btn3 = types.InlineKeyboardButton(chunk[i][2], callback_data=chunk[i][2])
                    cit1.append(btn3)
            markup.row(*cit1)
        bot.send_message(callback.message.chat.id, "Cool, please select From where", reply_markup=markup)

    elif data[0] == 'passenger':
        bot.send_message(callback.message.chat.id, "Cool, please input OK for next step, we need to "
                                                   "know where you want to ride.")
        bot.register_next_step_handler(callback.message, find_ftom_city)

    elif data[0] == 'prev' and data[1] == 'month':
        year, month = int(data[2]), int(data[3])
        month -= 1
        if month == 0:
            month = 12
            year -= 1
        markup = generate_calendar_keyboard(year, month)
        bot.edit_message_text("Please select a date:", callback.message.chat.id, callback.message.message_id,
                              reply_markup=markup)

    elif data[0] == 'next' and data[1] == 'month':
        year, month = int(data[2]), int(data[3])
        month += 1
        if month == 13:
            month = 1
            year += 1
        markup = generate_calendar_keyboard(year, month)
        bot.edit_message_text("Please select a date:", callback.message.chat.id, callback.message.message_id,
                              reply_markup=markup)

    elif data[0] == 'day':
        year, month, day = int(data[1]), int(data[2]), int(data[3])
        global ride_date
        ride_date = f"{year}-{month:02}-{day:02}"
        bot.send_message(callback.message.chat.id, f"Selected date: {ride_date}")
        bot.send_message(callback.message.chat.id, "Please write the number of free places 👤.")
        bot.register_next_step_handler(callback.message, free_places)

    elif callback.data in cities:
        if from_city_var == '':
            from_city_var = callback.data
            markup = types.InlineKeyboardMarkup()
            chunk = chunk_array(cities)
            for i in range(len(chunk)):
                btn1 = types.InlineKeyboardButton(chunk[i][0], callback_data=chunk[i][0])
                cit1 = [btn1]
                if len(chunk[i]) > 1:
                    btn2 = types.InlineKeyboardButton(chunk[i][1], callback_data=chunk[i][1])
                    cit1.append(btn2)
                    if len(chunk[i]) > 2:
                        btn3 = types.InlineKeyboardButton(chunk[i][2], callback_data=chunk[i][2])
                        cit1.append(btn3)
                markup.row(*cit1)
            bot.send_message(callback.message.chat.id, "Cool, please select To where", reply_markup=markup)
        elif to_city_var == '':
            to_city_var = callback.data
            today = datetime.date.today()
            markup = generate_calendar_keyboard(today.year, today.month)
            bot.send_message(callback.message.chat.id, "Please select a date:", reply_markup=markup)


def free_places(message):
    global places
    places = message.text
    bot.send_message(message.chat.id, "Write the price ֏ per passenger ")
    bot.register_next_step_handler(message, price_of_ride)


def price_of_ride(message):
    global price
    price = message.text
    bot.send_message(message.chat.id, "Write your car number.")
    bot.register_next_step_handler(message, car_number)


def car_number(message):
    global car_number
    car_number = message.text
    bot.send_message(message.chat.id, "Write your car mark.")
    bot.register_next_step_handler(message, car_mark)


def car_mark(message):
    global car_mark
    car_mark = message.text
    bot.send_message(message.chat.id, "Write your car color.")
    bot.register_next_step_handler(message, car_color)


def car_color(message):
    global from_city_var, to_city_var, ride_date, places, price, car_mark, car_number, car_color
    car_color = message.text
    bot.send_message(message.chat.id, f"Ok, we registered your ride:\n"
                                      f"From - {from_city_var}\n"
                                      f"To - {to_city_var}\n"
                                      f"Date - {ride_date}\n"
                                      f"Places - {places}\n"
                                      f"Price - {price}\n"
                                      f"Car - {car_mark} {car_number}, color {car_color}")


def find_ftom_city(message):
    global find_from_city
    find_from_city = message.text
    bot.send_message(message.chat.id, "Write from where you want to travel?")
    bot.register_next_step_handler(message, find_to_city)


def find_to_city(message):
    global find_to_city
    find_to_city = message.text
    bot.send_message(message.chat.id, "Write to where you want to travel?")
    bot.register_next_step_handler(message, find_date)


def find_date(message):
    global find_date
    find_date = message.text
    bot.send_message(message.chat.id, "Write when you want to travel?")
    bot.register_next_step_handler(message, find_places)


def find_places(message):
    global find_places
    find_places = message.text
    bot.send_message(message.chat.id, "Write how many places you need?")
    bot.register_next_step_handler(message, finish_ride_find)


def finish_ride_find(message):
    bot.send_message(message.chat.id, "OK, this is a list of rides.")


def chunk_array(array):
    return [array[i:i + 3] for i in range(0, len(array), 3)]


bot.polling(none_stop=True)
