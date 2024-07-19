from dotenv import load_dotenv
import os
import telebot
from controllers.driver_controller import DriverController
from controllers.passenger_controller import PassengerController
from configs.cities import cities
from components.start_buttons_component import generate_start_buttons

load_dotenv()

bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))
role = "none"

driver_handler = DriverController(bot)
passenger_handler = PassengerController(bot)


@bot.message_handler(commands=['start'])
def start(message):
    markup = generate_start_buttons(message)
    bot.send_message(message.chat.id, "Hello " + message.from_user.first_name +
                     ", I am your online friend. I will help you to find and create your ride. "
                     "Let me know, how you want to use the bot: as driver or as passenger?", reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback(callback):
    global role
    fullData = callback.data.split('_')
    data = fullData[0]
    if data == 'help':
        markup = generate_start_buttons(callback.message)
        bot.send_message(callback.message.chat.id, "You can find a ride on the way you need, "
                                                   "also you can share your rides with other users.",
                         reply_markup=markup)
    elif data == 'driver':
        if callback.message.chat.username is None:
            return bot.send_message(callback.message.chat.id, "Please add userName to your account")
        role = data
        driver_handler.start(callback.message)
    elif data == 'passenger':
        role = data
        passenger_handler.start(callback.message)
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
    elif data in ['prevRides', 'nextRides', 'firstRides', 'lastRides']:
        passenger_handler.handle_ride_find(callback.message, fullData[1])
    elif data == "showRide":
        passenger_handler.show_ride(callback.message, fullData[1])
    elif data == "bookRide":
        passenger_handler.book_ride(callback.message, fullData[1], fullData[2])
    elif data == "ridesList":
        pass
    elif data == "booksList":
        pass

    print(role, end="*****************\n\n")


bot.polling(none_stop=True)
