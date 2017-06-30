import psycopg2

from database_settings import db_settings


def connect_database():
    try:
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