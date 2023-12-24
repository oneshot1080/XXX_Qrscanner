import base64
from typing import Any
from PIL import Image
from io import BytesIO
from pyzbar.pyzbar import decode
import sqlite3 as sql

def process_data(data: Any):
    # Extract base64-encoded image data
    _, encoded_data = data.split(',', 1)
    image_data = base64.b64decode(encoded_data)

    image = Image.open(BytesIO(image_data))
    decoded_object  = decode(image)
    data = [obj.data.decode('utf-8') for obj in decoded_object]
    return data[0]

def valid_member(id: str):
    conn = sql.connect('sql.db')
    curs = conn.cursor()
    query = """SELECT access FROM members WHERE id = ?"""
    curs.execute(query, (id,))
    result = curs.fetchone()
    conn.commit()

    if result is None:
        curs.close()
        conn.close()
        return False
    else:
        if result[0] == 1:
            query = """UPDATE members SET access = 0 WHERE id = ?"""
            curs.execute(query, (id,))
            conn.commit()
        curs.close()
        conn.close()
        return result[0]