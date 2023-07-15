from deepface import DeepFace as dp
import cv2
import sqlite3 as sq
import checkphoto


def verify():
    try:
        cap = cv2.VideoCapture(0)

        for i in range(5):
            cap.read()

        img = cap.read()[1]

        cv2.imwrite('pic.jpg', img)

        cap.release()
        cv2.destroyAllWindows()
        with sq.connect("C:/Users/LyaKakoyPC/Desktop/employee.db") as con:
            cur = con.cursor()
            for art in cur.execute("SELECT face FROM person").fetchall():
                checkphoto.Write('pic1.jpg', art[0])
                if dp.verify(img1_path="pic.jpg", img2_path="pic1.jpg").get('verified'):
                    return True

    except Exception:
        return False
