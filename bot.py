import telebot
from handlers.driver_handler import DriverHandler
from handlers.passenger_handler import PassengerHandler
from handlers.booking_handler import BookingHandler
from utils.city_utils import cities
from utils.start_buttons_utils import generate_start_buttons

bot = telebot.TeleBot('7281065108:AAD2mn4uDewytqYRsTtR29SZ0-s8jBkCyA4')
role = "none"

driver_handler = DriverHandler(bot)
passenger_handler = PassengerHandler(bot)
booking_handler = BookingHandler(bot)


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
    elif data in ['prevRides', 'nextRides', 'firstRides', 'lastRides']:
        passenger_handler.handle_ride_find(callback.message, fullData[1])
    elif data == "showRide":
        passenger_handler.show_ride(callback.message, fullData[1])
    elif data == "bookRide":
        booking_handler.book_ride(callback.message, fullData[1], fullData[2])
    elif data == "ridesList":
        pass
    elif data == "booksList":
        pass

    print(role, end="*****************\n\n")


bot.polling(none_stop=True)
