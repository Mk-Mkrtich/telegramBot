import telebot
from telebot import types
from handlers.driver_handler import DriverHandler
from handlers.passenger_handler import PassengerHandler
from utils.city_utils import cities

bot = telebot.TeleBot('7281065108:AAD2mn4uDewytqYRsTtR29SZ0-s8jBkCyA4')

driver_handler = DriverHandler(bot)
passenger_handler = PassengerHandler(bot)

@bot.message_handler(commands=['start'])
def start(message):
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
    data = callback.data.split('_')[0]
    if data == 'help':
        bot.send_message(callback.message.chat.id, "You can find a ride on the way you need, "
                                                   "also you can share your rides with other users.")
    elif data == 'driver':
        driver_handler.start(callback.message)
    elif data == 'passenger':
        passenger_handler.start(callback.message)
    elif data in cities:
        driver_handler.handle_city_selection(callback.message, data)
    elif data in ['prev', 'next', 'day']:
        driver_handler.handle_calendar(callback)

bot.polling(none_stop=True)
