from telebot import types
from configs.storage import next, double_next, prev, double_prev

def generate(type):
    first_b = types.InlineKeyboardButton(f"{double_prev}", callback_data=f"{type}_first")
    prev_b = types.InlineKeyboardButton(f"{prev}", callback_data=f"{type}_prev")
    next_b = types.InlineKeyboardButton(f"{next}", callback_data=f"{type}_next")
    last_b = types.InlineKeyboardButton(f"{double_next}", callback_data=f"{type}_last")
    return [first_b, prev_b, next_b, last_b]

