import psycopg2


def get_db():
    schema = 'init.sql'
    conn = psycopg2.connect(database="user", user="peter", password="53a98wo", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    return conn
