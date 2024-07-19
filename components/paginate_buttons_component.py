from telebot import types


def generate(ride_len):
    if ride_len > 10:
        first_b = types.InlineKeyboardButton("⬅️⬅️", callback_data="firstRides_first")
        prev_b = types.InlineKeyboardButton("⬅️️", callback_data="prevRides_prev")
        next_b = types.InlineKeyboardButton("➡️", callback_data="nextRides_next")
        last_b = types.InlineKeyboardButton("➡️➡️", callback_data="lastRides_last")

        return [first_b, prev_b, next_b, last_b]
    return []
