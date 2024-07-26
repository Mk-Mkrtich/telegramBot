from dotenv import load_dotenv
import os
import telebot
from controllers.driver_controller import DriverController
from controllers.passenger_controller import PassengerController
from configs.cities import cities
from configs.storage import ids

load_dotenv()

bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))
role = "none"

driver_handler = DriverController(bot)
passenger_handler = PassengerController(bot)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello " + message.from_user.first_name +
                     "This is a start text about this bot")


@bot.message_handler(commands=['driver'])
def start(message):
    global role
    if message.chat.username is None:
        return ids.add(bot.send_message(message.chat.id, "Please add userName to your account").id)
    role = 'driver'
    driver_handler.clear_history(message.chat.id)
    driver_handler.start(message)


@bot.message_handler(commands=['passenger'])
def start(message):
    global role
    role = 'passenger'
    passenger_handler.clear_history(message.chat.id)
    passenger_handler.start(message)


@bot.message_handler(commands=['rideslist'])
def start(message):
    driver_handler.clear_history(message.chat.id)
    driver_handler.get_ride_list(message, "first")


@bot.message_handler(commands=['bookslist'])
def start(message):
    passenger_handler.get_books_list(message)


@bot.callback_query_handler(func=lambda callback: True)
def callback(callback):
    global role
    fullData = callback.data.split('_')
    print(fullData)
    data = fullData[0]
    if data == 'help':
        ids.add(bot.send_message(callback.message.chat.id, "You can find a ride on the way you need, "
                                                   "also you can share your rides with other users.").id)

    elif data == "fromCity" and fullData[1] in cities:
        if role == "driver":
            driver_handler.handle_from_city_selection(callback.message, fullData[1])
        else:
            passenger_handler.handle_from_city_selection(callback.message, fullData[1])
    elif data == "toCity" and fullData[1] in cities:
        if role == "driver":
            driver_handler.handle_to_city_selection(callback.message, fullData[1])
        else:
            passenger_handler.handle_to_city_selection(callback.message, fullData[1])
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
    elif data == "rides":
        passenger_handler.handle_ride_find(callback.message, fullData[1])
    elif data == "showRide":
        passenger_handler.show_ride(callback.message, fullData[1])
    elif data == "showRideDriver":
        driver_handler.show_ride(callback.message, fullData[1])
    elif data == "bookRide":
        passenger_handler.book_ride(callback.message, fullData[1], fullData[2])
    elif data == "ridesList":
        driver_handler.get_ride_list(callback.message, fullData[1])
    elif data == "booksList":
        passenger_handler.get_books_list(callback.message)
    elif data == "showBook":
        passenger_handler.show_book(callback.message, fullData[1])
    elif data == "cancelBook":
        passenger_handler.cancel_book(callback.message, fullData[1])

    print(role, end="*****************\n\n")


bot.polling(none_stop=True)
