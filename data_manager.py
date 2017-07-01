import os
import psycopg2
import urllib


def connect_database():
    try:
        urllib.parse.uses_netloc.append('postgres')
        url = urllib.parse.urlparse(os.environ.get('DATABASE_URL'))
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
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
