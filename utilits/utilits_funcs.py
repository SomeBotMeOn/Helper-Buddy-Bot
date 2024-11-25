import sqlite3

def personal_city(message):
    '''
    Функция для вызова города пользователя из базы данных
    '''
    num_id = message.chat.id
    conn = sqlite3.connect('../database/weather_outside.sqlite3')
    cur = conn.cursor()
    cur.execute("SELECT city FROM person WHERE id=?",(num_id,))
    result = cur.fetchone()
    city = result[0]
    return city