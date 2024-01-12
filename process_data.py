import base64
from typing import Any
import uuid
from PIL import Image
from io import BytesIO
from pyzbar.pyzbar import decode
import sqlite3 as sql
import qrcode


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
    
    
def add_one(name: str, email: str, ID: str):
    """Add one member to the table"""
    conn = sql.connect('sql.db')
    curs = conn.cursor()
    query = """INSERT INTO members ('name', 'email', 'id', 'access') VALUES (?, ?, ?, ?)"""
    try:
        curs.execute(query, ({name}, {email}, {ID}, 1))
        conn.commit()
        curs.close()
        conn.close()
    except Exception as e:
        print(e)
    
def add_many(path: str):
    """Add multiple members to the table from excel file
        path: Absolute path to the excel file
    """
    try:
        import pandas as pd
        df = pd.read_excel(path)
        for index, row in df.iterrows():
            name, email, sdt = row
            ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, sdt))
            add_one(name, email, ID)
    except Exception as e:
        print(e)
        
def extract_ID_and_create_QRCODE():
    conn = sql.connect('sql.db')
    curs = conn.cursor()
    query = """SELECT ID from members"""
    curs.execute(query)
    id_values = curs.fetchall()
    conn.commit()
    curs.close()
    conn.close()
    index = 1
    for ID in id_values:
        qrcode.make(ID).save(f'{index}.png')
        index += 1