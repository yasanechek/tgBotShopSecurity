import string
import random


def random_password():
    symbols_l = string.ascii_letters + string.digits
    symbols_p = string.ascii_letters + string.digits + string.punctuation
    password = ''
    login = ''
    for _ in range(8):
        password += random.choice(symbols_p)
    for _ in range(10):
        login += random.choice(symbols_l)
    return login, password


def code():
    s = ''
    for _ in range(4):
        s += random.choice(string.digits)
    return s
