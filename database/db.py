import sqlite3

# создание базы данных
conn = sqlite3.connect('users_db.sql')
cur = conn.cursor()
cur.execute(
    'CREATE TABLE IF NOT EXISTS users (id int, name varchar(50))'
)
conn.commit()
cur.close()
conn.close()