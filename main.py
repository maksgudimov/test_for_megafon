import psycopg2
from psycopg2 import Error
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import random

import datetime

scheduler = AsyncIOScheduler()
import logging
import asyncio

logging.basicConfig(level=logging.INFO,filename="logs.log",filemode="w")

DB_NAME = 'Tester'
DB_USER = 'maks'
DB_PASS = 'test'
DB_HOST = '45.146.164.55'
DB_PORT = '5432'

def connect():
    try:
        global conn, cursor
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS tableTest
        (
            id SERIAL PRIMARY KEY,
            data TEXT,
            date timestamp
        );"""
                       )
        conn.commit()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

def gener_str(number):
    str = ''
    for i in range(0, number):
        let = chr(random.randint(ord('a'), ord('z')))
        str += f"{let}"
    return str

async def insert_into_db():
    try:
        r = random.randint(1, 10)
        new_str = gener_str(r)
        sql_insert = """INSERT INTO tableTest(data,date) VALUES (%s, %s);"""
        item_purchase_time = datetime.datetime.now()
        item_insert = (new_str, item_purchase_time)
        cursor.execute(sql_insert, item_insert)
        conn.commit()
    except (Exception, Error) as error:
        print("Ошибка при insert с PostgreSQL", error)



async def select_from_db():
    cursor.execute(f"SELECT count(data) FROM tableTest;")
    (info,) = cursor.fetchone()
    print(f" count data == {info}")
    if info == 30:
        try:
            cursor.execute(f"DELETE FROM tableTest;")
            conn.commit()
            print("delete")
        except (Exception, Error) as error:
            print("Ошибка при insert с PostgreSQL", error)

def start_work_schedl():
    scheduler.add_job(insert_into_db, "interval", seconds=60)
    scheduler.add_job(select_from_db, "interval", seconds=62)
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    connect()
    start_work_schedl()

