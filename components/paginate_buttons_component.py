from telebot import types


def generate(type):
    first_b = types.InlineKeyboardButton("⬅️⬅️", callback_data=f"{type}_first")
    prev_b = types.InlineKeyboardButton("⬅️️", callback_data=f"{type}_prev")
    next_b = types.InlineKeyboardButton("➡️", callback_data=f"{type}_next")
    last_b = types.InlineKeyboardButton("➡️➡️", callback_data=f"{type}_last")
    return [first_b, prev_b, next_b, last_b]

