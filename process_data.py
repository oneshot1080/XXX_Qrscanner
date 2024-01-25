import base64
import time
from turtle import fillcolor
from typing import Any
import uuid
from PIL import Image
from io import BytesIO
from pyzbar.pyzbar import decode
import sqlite3 as sql
import qrcode
import ast
import threading


def process_data(data: Any):
    # Extract base64-encoded image data
    _, encoded_data = data.split(',', 1)
    image_data = base64.b64decode(encoded_data)

    image = Image.open(BytesIO(image_data))
    image.save("static/captured_image.png")
    decoded_object  = decode(image)
    data = [obj.data.decode('utf-8') for obj in decoded_object]
    data = ast.literal_eval(data[0])
    print(data[0])
    return data[0]

def set_access_0_(id: str):
    time.sleep(2)
    conn = sql.connect('sql.db')
    curs = conn.cursor()
    query = """UPDATE members SET access = 0 WHERE id = ?"""
    curs.execute(query, (id,))
    conn.commit()
    curs.close()
    conn.close()
    
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
            thread = threading.Thread(target=set_access_0_, args=(id,))
            thread.start()
        curs.close()
        conn.close()
        return result[0]
    
    
def add_one(name: str, email: str, ID: str):
    """Add one member to the table"""
    conn = sql.connect('sql.db')
    curs = conn.cursor()
    query = """INSERT INTO members ('name', 'email', 'id', 'access') VALUES (?, ?, ?, ?)"""
    try:
        curs.execute(query, (name, email, ID, 1))
        conn.commit()
    except Exception as e:
        print(e)
        query = """SELECT name FROM members WHERE id = ?"""
        curs.execute(query, (ID,))
        res = curs.fetchone()
        print(f'id {ID} has been used, member {name} use the same phone number as {res}')
    finally:
        curs.close()
        conn.close()

    
def add_many(path: str):
    """Add multiple members to the table from excel file

        path (param): Absolute path to the excel file
    """
    try:
        import pandas as pd
        df = pd.read_excel(path)
        for index, row in df.iterrows():
            name, email, sdt = row
            sdt = str(sdt)
            ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, sdt))
            add_one(name, email, ID)
    except Exception as e:
        print(e)

def delete_member(id: str):
    conn = sql.connect('sql.db')
    curs = conn.cursor()
    query = """DELETE FROM "members" WHERE id = ?"""
    try:
        curs.execute(query, (id,))
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        curs.close()
        conn.close()

def modify(id: str, info: str, value: str):
    if info == 'id':
        print("Access denied! ID can not be modified")
        return
    conn = sql.connect('sql.db')
    curs = conn.cursor()
    query = """UPDATE members SET ? = ? WHERE id = ?"""
    try:
        curs.execute(query, (info, value, id))
        conn.commit()

    except Exception as e:
        print(e)
    
    finally:
        curs.close()
        conn.close()

