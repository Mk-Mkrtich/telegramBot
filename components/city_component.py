from telebot import types

def generate_city_buttons(city_list, prefix):
    markup = types.InlineKeyboardMarkup()
    chunk = chunk_array(city_list)
    for i in range(len(chunk)):
        btn1 = types.InlineKeyboardButton(chunk[i][0], callback_data=prefix + "_" + str(chunk[i][0]))
        cit1 = [btn1]
        if len(chunk[i]) > 1:
            btn2 = types.InlineKeyboardButton(chunk[i][1], callback_data=prefix + "_" + str(chunk[i][1]))
            cit1.append(btn2)
            if len(chunk[i]) > 2:
                btn3 = types.InlineKeyboardButton(chunk[i][2], callback_data=prefix + "_" + str(chunk[i][2]))
                cit1.append(btn3)
        markup.row(*cit1)
    return markup

def chunk_array(array, chunk_size=3):
    return [array[i:i + chunk_size] for i in range(0, len(array), chunk_size)]
