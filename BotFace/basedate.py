import sqlite3 as sq

with sq.connect("C:/Users/LyaKakoyPC/Desktop/employee.db") as con:
    con.row_factory = sq.Row

    cur = con.cursor()

    person = cur.execute("SELECT * FROM person").fetchone()


