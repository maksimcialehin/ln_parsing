import psycopg2

from typing import List
from decouple import config


def get_info_about_app() -> List:
    with open('full_data.txt', mode='r', encoding='utf-8') as file:
        results = []
        for line in file:
            line = line.strip().split(';')
            results.append((line[1], line[2], line[3], line[4]))

    return results


def insert_data(record_to_insert) -> None:
    try:
        connection = psycopg2.connect(user=config('DB_USER'),
                                    password=config('DB_PASSWORD'),
                                    host="127.0.0.1",
                                    port=config('DB_PORT'),
                                    database=config('DB_NAME'))
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO business_apps_app (app_name, company_name, release_year, email) VALUES (%s,%s,%s,%s)"""
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into app table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into table", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


for app in get_info_about_app():
    print(app)
    insert_data(app)
