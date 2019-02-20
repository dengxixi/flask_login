import psycopg2


conn = psycopg2.connect(database="user", user="peter", password="53a98wo", host="127.0.0.1", port="5432")
cur = conn.cursor()


name = 'admin'
# cur.execute('insert into users (name, password) values (%s,%s)', ('admin', '123'))
# # print (user)
# conn.commit()
cur.execute('select * from users where name=%s', (name,))
rows = cur.fetchone()
print (type(rows[1]))
