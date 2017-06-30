import os
import psycopg2
import urllib
from database_settings import db_settings


def connect_database():
    try:
        if os.environ.get('https://data.heroku.com/datastores/7e0ef83c-9036-4b7f-83b4-e53f195186dc'):
            urllib.parse.uses_netloc.append('postgres')
            url = urllib.parse.urlparse(os.environ.get(
                'https://data.heroku.com/datastores/7e0ef83c-9036-4b7f-83b4-e53f195186dc'))
            conn = psycopg2.connect(
                database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port
            )
        else:
            # setup connection string
            connect_str = "dbname={} user={} host='localhost'".format(db_settings()['dbname'], db_settings()['user'])
            # use our connection values to establish a connection
            conn = psycopg2.connect(connect_str)
            # set autocommit option, to do every query when we call it
            conn.autocommit = True
            # create a psycopg2 cursor that can execute queries

        cursor = conn.cursor()

    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)

    return cursor, conn


def write_query(*query):
    try:
        cursor, conn = connect_database()
        cursor.execute(*query)
        return_message = True
    except Exception as e:
        print(e)
        return_message = False
    finally:
        if conn:
            conn.close()
    return return_message


def read_query(*query):
    try:
        cursor, conn = connect_database()
        cursor.execute(*query)
        row = cursor.fetchall()
        return row[0][0]
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()


def write_user(username, password):
    write_query("""INSERT INTO public.user (username, password)
               VALUES (%s, %s);""", (username, password))


def read_user_password(username):
    pass_hash_data = read_query("""SELECT password FROM public.user WHERE username = %s;""", (username,))
    if pass_hash_data:
        return pass_hash_data
    return
