from telebot import types


def generate_city_buttons(city_list, prefix):
    markup = types.InlineKeyboardMarkup()
    chunk = chunk_array(city_list)
    for i in range(len(chunk)):
        cit = []
        for city in chunk[i]:
            for city_id, city_info in city.items():
                btn = types.InlineKeyboardButton(city_info['name'], callback_data=prefix + "_" + city_id)
                cit.append(btn)
        markup.row(*cit)
    return markup


def chunk_array(array, chunk_size=3):
    return [array[i:i + chunk_size] for i in range(0, len(array), chunk_size)]
