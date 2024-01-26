from PIL import Image
import sqlite3 as sql
from QR import QR


def extract_ID_and_create_QRCODE():
    conn = sql.connect('sql.db')
    curs = conn.cursor()
    query = """SELECT ID from members"""
    curs.execute(query)
    id_values = curs.fetchall()
    conn.commit()
    curs.close()
    conn.close()
    ticket = Image.open('420171276_218935001215342_6328032920352527963_n.jpg')
    index = 1


    for ID in id_values:
        qr = QR(ID)
        qr = qr.resize((77, 77))
        ticket.paste(qr, (352, 90))
        ticket.save(f'QRCODES/online/{index}.png')
        index += 1
