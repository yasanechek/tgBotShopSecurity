import sqlite3 as sq


def code(password, key):
    key = str(key)
    pas = ''.join(list(map(lambda x: chr(ord(x) + int(key[0]) + int(key[-1])), [c for c in password])))
    return pas


def u_code(password, key):
    key = str(key)
    pas = ''.join(list(map(lambda x: chr(ord(x) - (int(key[0]) + int(key[-1]))), password)))
    return pas
