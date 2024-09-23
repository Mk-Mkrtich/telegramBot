from telebot import types
from configs.storage import colors


def generate_color_buttons():
    markup = types.InlineKeyboardMarkup()
    buttons = []

    for key, value in colors.items():
        buttons.append(types.InlineKeyboardButton(value + " " + key, callback_data="setColor_" + key))

        if len(buttons) % 2 == 0:
            markup.row(*buttons)
            buttons = []

    if buttons:
        markup.row(*buttons)

    return markup
