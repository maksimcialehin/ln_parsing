import sqlite3
from sqlite3 import Error
from typing import List


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def insert_data(conn, task):
    sql = ''' INSERT INTO business_apps_app(app_name, company_name, release_year, email)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid


def get_info_about_app() -> List:
    with open('full_data.txt', mode='r', encoding='utf-8') as file:
        results = []
        for line in file:
            line = line.strip().split(';')
            results.append((line[1], line[2], line[3], line[4]))

    return results


db = r'db.sqlite3'


conn = create_connection(db)

for app in get_info_about_app():
    print(app)
    insert_data(conn, app)
