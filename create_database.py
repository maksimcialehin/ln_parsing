import psycopg2

from psycopg2 import Error
from decouple import config


try:
    connection = psycopg2.connect(user=config('DB_USER'),
                                  password=config('DB_PASSWORD'),
                                  host="127.0.0.1",
                                  port=config('DB_PORT'),
                                  database=config('DB_NAME'))

    cursor = connection.cursor()
    
    # SQL query to create a new table
    create_table_query = '''CREATE TABLE business_apps_app
          (ID SERIAL PRIMARY KEY     NOT NULL,
          APP_NAME        TEXT    NOT NULL,
          COMPANY_NAME    TEXT    NOT NULL,
          RELEASE_YEAR    INT     ,
          EMAIL           TEXT); '''
    
    # Execute a command: this creates a new table
    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully in PostgreSQL ")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
