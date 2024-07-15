import types

import telebot
from telebot import types
from handlers.driver_handler import DriverHandler
from handlers.passenger_handler import PassengerHandler
from utils.city_utils import cities

bot = telebot.TeleBot('7281065108:AAD2mn4uDewytqYRsTtR29SZ0-s8jBkCyA4')
role = "none"

driver_handler = DriverHandler(bot)
passenger_handler = PassengerHandler(bot)

@bot.message_handler(commands=['start'])
def start(message):
    username = "none"
    if message.from_user.username is not None:
        username = message.from_user.username
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("I don't know what it is", callback_data='help'))
    btn1 = types.InlineKeyboardButton("I am a Driver", callback_data='driver_' + username)
    btn2 = types.InlineKeyboardButton("I am a Passenger", callback_data='passenger')
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id, "Hello " + message.from_user.first_name +
                     ", I am your online friend. I will help you to find and create your ride. "
                     "Let me know, how you want to use the bot: as driver or as passenger?", reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback(callback):
    global role
    fullData = callback.data.split('_')
    data = fullData[0]
    if data == 'help':
        bot.send_message(callback.message.chat.id, "You can find a ride on the way you need, "
                                                   "also you can share your rides with other users.")
    elif data == 'driver':
        if fullData[1] == 'none':
            return bot.send_message(callback.message.chat.id, "Please add userName to your account")
        role = "driver"
        driver_handler.start(callback.message)
    elif data == 'passenger':
        role = "passenger"
        passenger_handler.start(callback.message)
    elif data in cities:
        if role == "driver":
            driver_handler.handle_city_selection(callback.message, data)
        else:
            passenger_handler.handle_city_selection(callback.message, data)
    elif data in ['prev', 'next', 'day']:
        if role == "driver":
            driver_handler.handle_calendar(callback)
        else:
            passenger_handler.handle_calendar(callback)
    elif data == "passengersCount":
        if role == "driver":
            driver_handler.set_places(callback.message, fullData[1])
        else:
            passenger_handler.finish_ride_find(callback.message, fullData[1])
            role = "none"
    elif data == "priceData":
        driver_handler.set_price(callback.message, fullData[1])
        role = "none"

    print(role, end="*****************\n\n")


bot.polling(none_stop=True)
