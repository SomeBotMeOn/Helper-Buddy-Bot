from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# функция создания личной таблицы данных пользователя
def personal_classification(num_id):

    conn = sqlite3.connect('../database/weather_outside.sqlite3')
    cur = conn.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS 'weather_%d' (\
        'main'	NUMERIC(6, 3),\
        'temp'	NUMERIC(6, 3),\
        'temp_min'	NUMERIC(6, 3),\
        'temp_max'	NUMERIC(6, 3),\
        'humidity'	NUMERIC(6, 3),\
        'wind_speed'	NUMERIC(6, 3),\
        'clouds'	NUMERIC(6, 3),\
        'clothes_type'	INTEGER)" % num_id)
    conn.commit()

    cur.execute("INSERT INTO 'weather_%d' SELECT * FROM 'weather'" % num_id)
    conn.commit()
    cur.close()
    conn.close()