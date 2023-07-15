import telebot
from telebot import types

bot = telebot.TeleBot('5242198949:AAFIArP2YO-ktVHvtj_KHFNWcNRBZRdb6Bk')

keyboard = types.InlineKeyboardMarkup()
k1 = types.InlineKeyboardButton("Добавить машину в магазин", callback_data=1)
k2 = types.InlineKeyboardButton("Поменять цену")
k3 = types.InlineKeyboardButton("Добавить клиента в черный список", callback_data=2)
k4 = types.InlineKeyboardButton("Узнать прибыль", callback_data=3)
k5 = types.InlineKeyboardButton("Нанять помощника", callback_data=4)
keyboard.add(k1, k2, k3, k4, k5)
bot.send_message(1080152821, "Здравствуйте, всемогущий", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def call_(call):
    if call.data == '1':
        pass

