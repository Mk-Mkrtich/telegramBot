from telebot import types


def generate(ride_len, role):
    if ride_len > 10 and role == "passenger":
        first_b = types.InlineKeyboardButton("⬅️⬅️", callback_data="rides_first")
        prev_b = types.InlineKeyboardButton("⬅️️", callback_data="rides_prev")
        next_b = types.InlineKeyboardButton("➡️", callback_data="rides_next")
        last_b = types.InlineKeyboardButton("➡️➡️", callback_data="rides_last")
    else:
        first_b = types.InlineKeyboardButton("⬅️⬅️", callback_data="ridesList_first")
        prev_b = types.InlineKeyboardButton("⬅️️", callback_data="ridesList_prev")
        next_b = types.InlineKeyboardButton("➡️", callback_data="ridesList_next")
        last_b = types.InlineKeyboardButton("➡️➡️", callback_data="ridesList_last")
        return [first_b, prev_b, next_b, last_b]
    return []
