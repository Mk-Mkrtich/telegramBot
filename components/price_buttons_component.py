from telebot import types


def generate_price_buttons():
    markup = types.InlineKeyboardMarkup()
    passengers_count = []
    for i in range(3, 8):
        btn = types.InlineKeyboardButton(str(i * 100) + " ֏", callback_data="priceData_" + str(i * 100))
        passengers_count.append(btn)
    markup.row(*passengers_count)
    passengers_count = []
    for i in range(8, 13):
        btn = types.InlineKeyboardButton(str(i * 100) + " ֏", callback_data="priceData_" + str(i * 100))
        passengers_count.append(btn)
    markup.row(*passengers_count)

    return markup
