import telebot
from telebot import types
import sqlite3 as sq

import check
import password

bot = telebot.TeleBot('5242198949:AAFIArP2YO-ktVHvtj_KHFNWcNRBZRdb6Bk')


def reg(message):
    p_a_l = password.random_password()
    info_users = tuple(message.text.split()) + p_a_l
    with sq.connect("C:/Users/LyaKakoyPC/Desktop/Cars.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO users(surname, name, lastname, card, login, password) VALUES(?, ?, ?, ?, ?, ?)",
                    info_users)
    bot.send_message(message.chat.id, f"Ваш логин: {p_a_l[0]}\nВаш пароль: {p_a_l[1]}")


def enter(message):
    l_a_p = message.text.split()
    flag = True
    with sq.connect("C:/Users/LyaKakoyPC/Desktop/Cars.db") as con:
        cur = con.cursor()
        for n, person in enumerate(cur.execute("SELECT name, lastname, login, password FROM users").fetchall(),
                                   start=1):
            if l_a_p[0] == person[2] and l_a_p[1] == person[3]:
                flag = False
                bot.send_message(message.chat.id, f"Здравствуйте, {person[0]} {person[1]}!")

    if flag:
        keyboard = types.InlineKeyboardMarkup()
        k1 = types.InlineKeyboardButton("Выбрать машину", callback_data=1)
        k2 = types.InlineKeyboardButton("sms-оповещения", callback_data=2)
        k3 = types.InlineKeyboardButton("Начать поездку", callback_data=3)
        k4 = types.InlineKeyboardButton("Закончить поездку", callback_data=4)
        keyboard.add(k1, k2, k3, k4)
        bot.send_message(message.chat.id, "Вы ввели неправильно логин или пароль. Попробуйте войти ещё раз", reply_markup=keyboard)


@bot.message_handler(commands=['admin'])
def admin(message):
    res = check.verify()
    if res:
        keyboard = types.InlineKeyboardMarkup()
        k1 = types.InlineKeyboardButton("Добавить машину в магазин", callback_data=1)
        k2 = types.InlineKeyboardButton("Поменять цену")
        k3 = types.InlineKeyboardButton("Добавить клиента в черный список", callback_data=2)
        k4 = types.InlineKeyboardButton("Узнать прибыль", callback_data=3)
        k5 = types.InlineKeyboardButton("Нанять помощника", callback_data=4)
        keyboard.add(k1, k2, k3, k4, k5)
        bot.send_message(message.chat.id, "Здравствуйте, всемогущий", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Извините, но у вас нет доступа")


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    k1 = types.KeyboardButton("Войти в аккаунт")
    k2 = types.KeyboardButton("Зарегистрироваться")
    keyboard.add(k1, k2)
    bot.send_message(message.chat.id, "Здравствуйте, мы огромная сеть каршеринга! Создайте свой аккаунт для аренды "
                                      "автомобиля или зайдите в уже существующий", reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == "Войти в аккаунт":
        bot.send_message(message.chat.id, "Введите логин и пароль(через пробел)")
        bot.register_next_step_handler(message, enter)
    elif message.text == "Зарегистрироваться":
        bot.send_message(message.chat.id, "Введите своё Ф.И.О и номер карты(через пробел)")
        bot.register_next_step_handler(message, reg)


bot.polling(none_stop=True)
