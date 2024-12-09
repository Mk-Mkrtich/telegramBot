ids = set()
cash = dict()
car = "🚗"
date = "📅"
time = ""
start = "📍"
finish = "->"
can_not = "❗️"
price = "💸"
passenger = "👤"
next = "➡️"
double_next = "➡️➡️"
prev = "⬅️"
double_prev = "⬅️⬅️"
to_back = "👈 Back"
to_cancel = "🚫Cancel"

times = {
    "00:00": "🌙",
    "01:00": "🌙",
    "02:00": "🌙",
    "03:00": "🌙",
    "04:00": "🌙",
    "05:00": "🌙",
    "06:00": "☀️",
    "07:00": "☀️",
    "08:00": "☀️",
    "09:00": "☀️",
    "10:00": "☀️",
    "11:00": "☀️",
    "12:00": "☀️",
    "13:00": "☀️",
    "14:00": "☀️",
    "15:00": "☀️",
    "16:00": "☀️",
    "17:00": "☀️",
    "18:00": "☀️",
    "19:00": "☀️",
    "20:00": "🌙",
    "21:00": "🌙",
    "22:00": "🌙",
    "23:00": "🌙",
}

colors = {
    "White": "Սպիտակ ⚪",
    "Silver": "Արծաթագույն ⚪",
    "Gray": "Մոխրագույն ⚪",
    "Black": "Սև ⚫",
    "Brown": "Շագանակագույն 🟤",
    "Golden": "Ոսկեգույն 🟡",
    "Beige": "Բեժ ⚪",
    "Red": "Կարմիր 🔴",
    "Blue": "Կապույտ 🔵",
    "Orange": "Նարնջագույն 🟠",
    "Yellow": "Դեղին 🟡",
    "Green": "Կանաչ 🟢",
    "Sky": "Երկնագույն 🔵",
    "Bordeaux": "Բորդո 🔴",
    "Pink": "Վարդագույն 🔴",
    "Purple": "Մանուշակագույն 🟣",
}

user_ratings = {
    0: "🟢",
    1: "🟠",
    2: "🔴",
    3: "⚫"
}

user_ratings_text = {
    0: f" {user_ratings[0]} Good ",
    1: f" {user_ratings[1]} Normal",
    2: f" {user_ratings[2]} Bad",
    3: f" {user_ratings[3]} Դուք արգելափակված եք բացասական կարծիքների պատճառով։ Մինչև "
}

months = {
    "January": "Հունվար",
    "February": "Փետրվար",
    "March": "Մարտ",
    "April": "Ապրիլ",
    "May": "Մայիս",
    "June": "Հունիս",
    "July": "Հուլիս",
    "August": "Օգոստոս",
    "September": "Սեպտեմբեր",
    "October": "Հոկտեմբեր",
    "November": "Նոյեմբեր",
    "December": "Դեկտեմբեր",
}

commandList = ['start', 'help', 'driver', 'passenger', 'support', 'rideslist', 'bookslist']
