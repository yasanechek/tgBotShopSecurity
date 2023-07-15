import sqlite3 as sq

with sq.connect("C:/Users/LyaKakoyPC/Desktop/Cars.db") as con:
    cur = con.cursor()

    cars_info = cur.execute("SELECT * FROM car").fetchall()

    def price(name):
        return cur.execute(f"SELECT price FROM car WHERE model = {name}").fetchone()[0]

    cars_name = [c[0] for c in cars_info]

