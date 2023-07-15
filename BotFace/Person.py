import sqlite3 as sq


def AllPerson():
    with sq.connect("C:/Users/LyaKakoyPC/Desktop/employee.db") as con:
        cur = con.cursor()

        cur.execute("SELECT name, surname FROM person").fetchall()


