from dotenv import load_dotenv
import os
import telebot
from telebot import types
from controllers.booking_controller import BookingController
from controllers.driver_controller import DriverController
from controllers.passenger_controller import PassengerController
from controllers.ride_controller import RideController
from controllers.supoport_controller import SupportController
from configs.storage import ids, next, user_ratings, can_not, commandList, cash
from repository.user_repository import UserRepository

load_dotenv()

bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))

driver_handler = DriverController(bot)
ride_handler = RideController(bot)
booking_handler = BookingController(bot)
passenger_handler = PassengerController(bot)
support_handler = SupportController(bot)
user = UserRepository()


@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact is not None:
        checked_user = user.check_user(message)
        if checked_user['ok']:
            bot.send_message(message.chat.id,
                             f"Thank you for sharing your phone number: now you can continue using the bot")
        else:
            bot.send_message(message.chat.id,
                             f"somthing went wrong, please try later")


@bot.message_handler(commands=commandList)
def start(message):
    checked_user = user.check_user(message)
    if checked_user['ok']:
        command = message.text[1:]
        commands_dict = {
            'start': start_function,
            'help': help,
            'driver': driver,
            'passenger': passenger,
            'rideslist': rideslist,
            'bookslist': bookslist,
        }

        if command in commands_dict:
            commands_dict[command](message)
        if cash.get(message.chat.id):
            cash.pop(message.chat.id)
    else:
        if checked_user['message'] == 'contact':
            ids.add(bot.send_message(message.chat.id,
                                     "Խնդրում ենք ավելացնել օգտատիրոջ անուն՝ \n\n օրինակ @find_way_arm_bot, kam "
                                     "karox eq poxancel dzer heraxosahamar@").id)
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            button_phone = types.KeyboardButton(text="Share phone number", request_contact=True)
            markup.add(button_phone)
            bot.send_message(message.chat.id, "sexmelov aystex ⬇️:", reply_markup=markup)


def bookslist(message):
    booking_handler.clear_history(message.chat.id)
    booking_handler.get_booking_list(message)


def rideslist(message):
    ride_handler.clear_history(message.chat.id)
    ride_handler.get_ride_list(message, 'driver')


def passenger(message):
    passenger_handler.clear_history(message.chat.id)
    user.set_role(message.chat.id, 'passenger')
    passenger_handler.start(message)


def driver(message):
    driver_handler.clear_history(message.chat.id)
    user.set_role(message.chat.id, 'driver')
    driver_handler.start(message)

def help(message):
    driver_handler.clear_history(message.chat.id)
    ids.add(message.message_id)
    text1 = ("Եթե դուք վարորդ եք, կարող եք հրապարակել ձեր ուղևորությունները այստեղ՝ նշելով քաղաքները,"
             " ուղևորության օրը և ժամը, ուղևորների քանակը, որոնց կարող եք վերցնել, գինը, որով ցանկանում եք "
             "գնալ, ինչպես նաև մեքենայի գույնը, մոդելը և պետհամարանիշը։ Ուղևորները, որոնք կկարողանան "
             "ամրագրել տեղեր, կտեսնեն բոլոր տեղեկությունները՝ բացառությամբ ձեր կոնտակտների։ "
             "Կոնտակտները տեսանելի կդառնան ամրագրումից հետո, իսկ դուք ծանուցում կստանաք "
             "ինչպես ամրագրման, այնպես էլ չեղարկման դեպքում։ \n\n")
    text2 = ("Եթե դուք ուղևոր եք, կարող եք նշել քաղաքները, ուղևորության օրը և անհրաժեշտ տեղերի քանակը։"
             "Ապա դուք կտեսնեք ուղևորությունների ցանկը, որտեղ ցուցադրվում է վարորդների վարկանիշը "
             "և այլ մանրամասներ ուղևորության մասին\n\n"
             f" {user_ratings[0]} - լավ "
             f" {user_ratings[1]} - ընդունելի "
             f" {user_ratings[2]} - վատ\n\n"
             "Ներկայացված տեղեկություններով, դուք կարող եք ընտրել տեղերի քանակը ամրագրելու համար։"
             " Վարորդը կստանա ծանուցում ձեր կոնտակտային տվյալներով, իսկ դուք,"
             " իր հերթին, կստանաք վարորդի կոնտակտները։")
    text3 = (f"{can_not}{can_not} Սա հարթակ է, որը թույլ է տալիս վարորդներին "
             f"և ուղևորներին գտնել միմյանց և համաձայնեցնել ճանապարհորդության "
             f"մանրամասները: Բոտը պատասխանատու չէ և պարտավորություններ չունի։ "
             f"Վճարումը կատարվում է ուղևորի և վարորդի համաձայնությամբ։ Բոտը ֆինանսական "
             f"շահ չի հետապնդում, և հարթակը լիովին անվճար է:"
             f" Դուք կարող եք կապվել աջակցության թիմի հետ՝ արգելափակելու անպատշաճ "
             f"օգտատերերին, ինչը կօգնի բարելավել հարթակը {can_not}{can_not}\n\n:"
             "Բարի ճանապարհորդություն")
    ids.add(bot.send_message(message.chat.id, text1).id)
    ids.add(bot.send_message(message.chat.id, text2).id)
    ids.add(bot.send_message(message.chat.id, text3).id)


def start_function(message):
    text = (f"Բարև հարգելի  {message.from_user.first_name}, բարի գալուստ Հայաստանի ամենահեշտ, ամենահարմար և "
            "օգտակար բոտը, այստեղ միայն իրական մարդիկ են, ովքեր փնտրում են"
            " վարորդներ կամ ուղևորներ՝ միմյանց օգնելու և ճանապարհորդության արժեքը"
            " նվազեցնելու համար. \n\n\n"
            f"{can_not}{can_not} Բոտը պատասխանատու չէ և պարտավորություններ չունի։ "
            f"Վճարումը կատարվում է ուղևորի և վարորդի համաձայնությամբ։ Բոտը ֆինանսական "
            f"շահ չի հետապնդում, և հարթակը լիովին անվճար է:{can_not}{can_not} "
            f"Լրացուցիչ տեղեկությունների համար սեղմեք այստեղ {next} /help \n\n"
            f"եթե ցանկանում եք վարորդ գտնել` սեղմեք այստեղ {next} /passenger \n\n"
            f"եթե ցանկանում եք գտնել ուղևորներ` սեղմեք այստեղ {next} /driver \n\n"
            f"Կարող եք տեսնել ձեր ամրագրված տեղերը՝ սեղմելով այստեղ {next} /bookslist \n\n"
            f"Դուք կարող եք գտնել ձեր ճանապարհորդությունները՝ սեղմելով այստեղ {next} /rideslist \n\n"

            f"Փորձեք նաև գտնել այս հրամանը ներքևի ձախ անկյունում՝ սեղմելով ցանկի կոճակը ↙️")
    bot.send_message(message.chat.id, text)


@bot.callback_query_handler(func=lambda callback: True)
def callback(callback):
    role = user.get_role(callback.message.chat.id)
    fullData = callback.data.split('_')
    print(fullData)
    data = fullData[0]
    if data == "fromCity":
        if role == "driver":
            driver_handler.handle_from_city_selection(callback.message, fullData[1])
        else:
            passenger_handler.handle_from_city_selection(callback.message, fullData[1])
    elif data == "toCity":
        if role == "driver":
            driver_handler.handle_to_city_selection(callback.message, fullData[1])
        else:
            passenger_handler.handle_to_city_selection(callback.message, fullData[1])
    elif data in ['prev', 'next', 'day']:
        if role == "driver":
            driver_handler.handle_calendar(callback, role)
        else:
            passenger_handler.handle_calendar(callback, role)
    elif data == "fideTime":
        driver_handler.handle_time(callback, fullData[1])
    elif data == "passengersCount":
        if role == "driver":
            driver_handler.set_places(callback.message, fullData[1])
        else:
            passenger_handler.finish_ride_find(callback.message, fullData[1])
            user.set_role(callback.message.chat.id, 'none')
    elif data == "priceData":
        driver_handler.set_price(callback.message, fullData[1])
        user.set_role(callback.message.chat.id, 'none')
    elif data == "setColor":
        driver_handler.set_color(callback.message, fullData[1])
        user.set_role(callback.message.chat.id, 'none')
    elif data == "baggage":
        driver_handler.set_baggage(callback.message, fullData[1])

    elif data == "userNewCar":
        driver_handler.set_new_car(callback.message, fullData[1])
    elif data == "userCar":
        driver_handler.publish_ride(callback.message, fullData[1], fullData[2])
    elif data == "showRide":
        ride_handler.show_ride(callback.message, fullData[1], fullData[2])
    elif data == "rideList":
        ride_handler.get_ride_list(callback.message, fullData[1])
    elif data == "cancelRide":
        ride_handler.cancel_ride(callback.message, fullData[1])
    elif data == "bookRide":
        booking_handler.booking_ride(callback.message, fullData[1], fullData[2])
    elif data == "suggestRide":
        ride_handler.suggest_ride_list(callback.message, {"from_city_id": fullData[1], "to_city_id": fullData[2],
                                                          "date": fullData[3], "free_places": fullData[4]})
    elif data == "showBook":
        booking_handler.show_booking(callback.message, fullData[1])
    elif data == "booksList":
        booking_handler.get_booking_list(callback.message)
    elif data == "cancelBook":
        booking_handler.cancel_booking(callback.message, fullData[1])


bot.polling(none_stop=True)
