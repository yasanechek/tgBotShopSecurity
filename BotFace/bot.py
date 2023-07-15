import string
import hash_password
import telebot
from telebot import types
import sqlite3 as sq
import cars
import check
import password
from datetime import datetime
import pytz

bot = telebot.TeleBot('5242198949:AAFIArP2YO-ktVHvtj_KHFNWcNRBZRdb6Bk')


def add(message):
    mes = message.text.split()
    car = (' '.join(mes[0:-1]), mes[-1])
    with sq.connect("C:/Users/LyaKakoyPC/Desktop/Cars.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO car(model, price, count) VALUES(?, ?, 1)", car)
    bot.send_message(message.chat.id, "Машина добавлена")


def change(message):
    new = message.text.split()
    with sq.connect("C:/Users/LyaKakoyPC/Desktop/Cars.db") as con:
        cur = con.cursor()
        cur.execute(f"UPDATE car SET price = {new[-1]} WHERE car.model = '{' '.join(new[0:-1])}' ")
    bot.send_message(message.chat.id, "Изменения сохранены")


def add_k(message):
    with sq.connect("C:/Users/LyaKakoyPC/Desktop/Cars.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO black_list VALUES(?)", (message.text,))
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, f"{message.text} добавлен в черный список")


def reg(message):
    id_ = message.chat.id
    info = message.text.split()
    if len(info) != 4:
        bot.send_message(id_, "Неправильный ввод данных\nПример: Иванов Иван Иванович 2365674327845673")
        return
    fio = ''.join(info[0:-1])
    for num in string.digits:
        if num in fio:
            bot.send_message(id_, "Неправильный ввод данных\nПредупреждение: видимо вы использовали цифры в записи "
                                  "Ф.И.О")
            return
    rus = 'ёйцукенгшщзхъфывапролджэячсмитьбю'
    for num in str(info[-1]):
        if num in string.ascii_letters + rus + rus.upper():
            bot.send_message(id_, "Неправильный ввод данных\nПредупреждение: видимо вы использовали буквы в записи "
                                  "номера карты")
            return
    p_a_l = password.random_password()
    info_users = tuple(info) + (hash_password.code(p_a_l[0], info[-1]), hash_password.code(p_a_l[-1], info[-1]), id_)
    with sq.connect("C:/Users/LyaKakoyPC/Desktop/Cars.db") as con:
        cur = con.cursor()
        flag = True
        for id in cur.execute("SELECT id FROM users"):
            if id_ == id[0]:
                flag = False
        if flag:
            cur.execute("INSERT INTO users(surname, name, lastname, card, login, password, id) VALUES(?, ?, ?, ?, "
                        "?, "
                        "?, ?)",
                        info_users)
            bot.send_message(id_, f"Ваш <b>логин</b>: {p_a_l[0]}\nВаш <b>пароль</b>: {p_a_l[1]}", parse_mode='html')
            bot.send_message(id_, "<b>Предупреждение</b>:\n"
                                  "Рекомендуем запомнить данные и очистить историю, чтобы повысить безопасность", parse_mode='html')
        else:
            bot.send_message(id_, "Вы уже зарегистрированы")


def code(message, personal_code, name, surname):
    if message.text == personal_code:
        keyboard = types.InlineKeyboardMarkup()
        k1 = types.InlineKeyboardButton("Выбрать машину", callback_data=1)
        k2 = types.InlineKeyboardButton("sms-оповещения", callback_data=2)
        keyboard.add(k1, k2)
        bot.send_message(message.chat.id, f"Здравствуйте, {name} {surname}!", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "<b>Неверный код</b>", parse_mode='html')


def enter(message):
    bot.delete_message(message.chat.id, message.message_id)
    id_ = message.chat.id
    l_a_p = message.text.split()
    flag = True
    with sq.connect("C:/Users/LyaKakoyPC/Desktop/Cars.db") as con:
        cur = con.cursor()
        for id in cur.execute("SELECT id FROM black_list"):
            if id_ == id[0]:
                bot.send_message(id_, "Кажется вы неоднократно нарушали правила, поэтому вам запрещён доступ")
                return
        for n, person in enumerate(
                cur.execute("SELECT name, lastname, login, password, card, id FROM users").fetchall(),
                start=1):
            if l_a_p[0] == hash_password.u_code(person[2], person[4]) and l_a_p[1] == hash_password.u_code(person[3],
                                                                                                           person[
                                                                                                               4]) and \
                    person[5] == message.chat.id:
                flag = False
                keyboard = types.InlineKeyboardMarkup()
                k1 = types.InlineKeyboardButton("Выбрать машину", callback_data=1)
                k2 = types.InlineKeyboardButton("sms-оповещения", callback_data=2)
                k3 = types.InlineKeyboardButton("Выйти", callback_data='exists')
                keyboard.add(k1, k2, k3)
                bot.send_message(message.chat.id, f"Здравствуйте, {person[0]} {person[1]}!", reply_markup=keyboard)

            elif l_a_p[0] == hash_password.u_code(person[2], person[4]) and l_a_p[1] == hash_password.u_code(person[3],
                                                                                                             person[
                                                                                                                 4]) and \
                    person[5] != message.chat.id:
                flag = False
                bot.send_message(id_, "Похоже вы входите с другого устройства, <b>напишите тут 4-х "
                                      "значный</b> код, который мы отправили на ваш телеграм, чтобы войти",
                                 parse_mode='html')
                personal_code = password.code()
                bot.send_message(person[5], f"Ваш код: <b>{personal_code}</b>", parse_mode='html')
                bot.register_next_step_handler(message, code, personal_code, person[0], person[1])

    if flag:
        bot.send_message(message.chat.id, "Вы ввели неправильно логин или пароль. Попробуйте войти ещё раз",
                         reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=['admin'])
def admin(message):
    bot.delete_message(message.chat.id, message.message_id)
    res = check.verify()
    if res:
        keyboard = types.InlineKeyboardMarkup()
        k1 = types.InlineKeyboardButton("Добавить машину в магазин", callback_data='add')
        k2 = types.InlineKeyboardButton("Поменять цену", callback_data='change')
        k3 = types.InlineKeyboardButton("Добавить клиента в черный список", callback_data='add_k')
        k4 = types.InlineKeyboardButton("Узнать прибыль", callback_data='profit')
        keyboard.add(k1, k2, k3, k4)
        bot.send_message(message.chat.id, "Здравствуйте, всемогущий", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Вам отказано в доступе")
        bot.send_message(1080152821, "В данный момент на ваш аккаунт хочет зайти: ")
        bot.send_photo(1080152821, open("pic.jpg", 'rb'))


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


@bot.callback_query_handler(func=lambda call: True)
def call_(call):
    if call.data == '1' or call.data == "Нет":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        keyboard = types.InlineKeyboardMarkup()
        with sq.connect("C:/Users/LyaKakoyPC/Desktop/Cars.db") as con:
            cur = con.cursor()
            for car in cur.execute("SELECT * FROM car").fetchall():
                k = types.InlineKeyboardButton("Модель: " + car[0] + " Цена: " + str(car[2]) + "руб. за 1 мин.",
                                               callback_data=car[0])
                keyboard.add(k)
        k = types.InlineKeyboardButton("Назад", callback_data='назад')
        keyboard.add(k)
        bot.send_message(call.message.chat.id, "Наши машины:", reply_markup=keyboard)
    elif call.data in cars.cars_name:
        keyboard = types.InlineKeyboardMarkup()
        k1 = types.InlineKeyboardButton("Да, все верно", callback_data="Да")
        k2 = types.InlineKeyboardButton("Нет, хочу другую машину", callback_data="Нет")
        keyboard.add(k1, k2)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f"Вы выбрали: <b>{call.data}</b>\nВсе верно?",
                         parse_mode='html', reply_markup=keyboard)
    elif call.data == "Да":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        keyboard = types.InlineKeyboardMarkup()
        k1 = types.InlineKeyboardButton("Начать поездку", callback_data="Старт")
        k2 = types.InlineKeyboardButton("Закончить поездку", callback_data="Стоп")
        keyboard.add(k1, k2)
        bot.send_message(call.message.chat.id, "Управление: ", reply_markup=keyboard)
    elif call.data == 'add':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Введите название машину и цену за 1 минуту(через пробел)")
        bot.register_next_step_handler(call.message, add)
    elif call.data == 'add_k':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Введите id человека, которого добавить в черный список")
        bot.register_next_step_handler(call.message, add_k)
    elif call.data == 'Старт':
        bot.send_message(call.message.chat.id, "Приятного пути!\nСпасибо что выбрали нас.")
        t = datetime.now(pytz.timezone('Europe/Moscow'))
        bot.send_message(call.message.chat.id, f"Время начало поездки: {t}")
    elif call.data == 'Стоп':
        bot.send_message(call.message.chat.id, "Поездка окончена!")
        t = datetime.now(pytz.timezone('Europe/Moscow'))
        bot.send_message(call.message.chat.id, f"Время конца поездки: {t}")
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data == 'change':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Введите название машины и новую цену(через пробел)")
        bot.register_next_step_handler(call.message, change)

    elif call.data == 'exists':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Ждём вас ещё!", reply_markup=types.ReplyKeyboardRemove())

    elif call.data == 'назад':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        keyboard = types.InlineKeyboardMarkup()
        k1 = types.InlineKeyboardButton("Выбрать машину", callback_data=1)
        k2 = types.InlineKeyboardButton("sms-оповещения", callback_data=2)
        k3 = types.InlineKeyboardButton("Выйти", callback_data='exists')
        keyboard.add(k1, k2, k3)
        bot.send_message(call.message.chat.id, '<b>Главное меню</b>', reply_markup=keyboard, parse_mode='html')


bot.polling(none_stop=True)
