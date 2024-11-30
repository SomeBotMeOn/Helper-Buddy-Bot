from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import sqlite3
from handlers.weather_functions.weather import get_current_weather
from bot_instance import bot

weather_main_codes = ['Clear', 'Clouds', 'Drizzle', 'Rain', 'Snow', 'Thunderstorm']

def personal_cloth(message):
    # функция достает из БД город пользователя и передает в knn, а затем выводим одежду пользователю
    num_id = message.chat.id
    conn = sqlite3.connect('../database/weather_outside.sqlite3')
    cur = conn.cursor()
    cur.execute("SELECT city FROM person WHERE id=?",
                (num_id,))
    result = cur.fetchone()
    city = result[0]
    cur_weather = get_current_weather(city)
    main_weather = weather_main_codes.index(cur_weather['weather'][0]['main'])
    temp_weather = cur_weather['main']['temp']
    temp_min_weather = cur_weather['main']['temp_min']
    temp_max_weather = cur_weather['main']['temp_max']
    humidity_weather = cur_weather['main']['humidity']
    wind_speed_weather = cur_weather['wind']['speed']
    clouds_weather = cur_weather['clouds']['all']
    x_test = pd.DataFrame([main_weather, temp_weather, temp_min_weather, temp_max_weather, humidity_weather, wind_speed_weather, clouds_weather])
    final_cloth = knn_and_rewrite(num_id, x_test) # вызываем knn
    bot.send_message(message.chat.id, final_cloth[0]) # выводим пользователю одежду
    sql = "INSERT INTO weather_{d} (main, temp, temp_min, temp_max, humidity, wind_speed, clouds, clothes_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?);".format(
        d=num_id)
    params = (main_weather, temp_weather, temp_min_weather, temp_max_weather, humidity_weather, wind_speed_weather,
              clouds_weather, -1*(int(final_cloth[1])+1))
    cur.execute(sql, params)
    conn.commit()
    cur.close()
    conn.close()

# расшифровка индексов одежды
# расшифровка индексов одежды
clothes_codes = [
    'свитер/худи\n зимняя куртка/пуховик\n шапка\n шарф🧣\n перчатки🧤',
    "лонгслив/легкий свитер\n зимняя куртка/пуховик🧥\n шапка\n шарф🧣",
    "свитер/худи\n пальто/куртка🧥\n шапка\n шарф",
    "лонгслив/легкий свитер\n пальто/куртка🧥",
    "свитер/худи\n ветровка/плащ🧥",
    "майка/футболка/лонгслив👕\n ветровка/плащ🧥",
    "майка/футболка/лонгслив👕\n свитер/худи",
    "майка/футболка/лонгслив👕\n кофта/пиджак",
    "свитер/худи",   
    "футболка/лонгслив/легкий свитер 👚👖",
    "майка/футболка 👕🩳"
]


def processing_callback_results(num_id, num_items):
    print('ok0')
    # преобразуем значение num_items под коэффициент на который надо умножать
    num_strings = abs(num_items - 2)*2 + 1
    conn = sqlite3.connect('../database/weather_outside.sqlite3')
    cur = conn.cursor()
    print('ok1')

    # Выбираем строки с отрицательными значениями в clothes_type
    query = f"SELECT * FROM 'weather_{num_id}' WHERE clothes_type < 0;"
    cur.execute(query)
    print('ok2')
    # Получаем все строки с отрицательными значениями
    rows = cur.fetchall()

    if len(rows) > 0:
        # Изменяем значение clothes_type, умножив его на -1
        updated_rows = []
        for row in rows:
            new_row = list(row)
            new_row[-1] = new_row[-1] * (-1) -1 # Умножаем последний элемент (clothes_type) на -1 и вычитаем 1
            print('ok3')
            #преобразуем в то, что было бы надеть комфортнее, если предсказание не совпало
            if num_items == 0:
                if new_row[-1] + 2 >= 10: new_row[-1] = 10
                else: new_row[-1] += 2

            if num_items == 1:
                if new_row[-1] + 1 >= 10: new_row[-1] = 10
                else: new_row[-1] += 1

            if num_items == 3:
                if new_row[-1] - 1 <= 0:
                    new_row[-1] = 0
                else:
                    new_row[-1] -= 1

            if num_items == 4:
                if new_row[-1] - 2 <= 0:
                    new_row[-1] = 0
                else:
                    new_row[-1] -= 2

            updated_rows.append(new_row)


        # результат правильного предсказания будем сохранять только в случае, если длина таблицы менее 250
        # Запрашиваем количество строк в таблице
        cur.execute(f"SELECT COUNT(*) FROM 'weather_{num_id}';")
        count_table_strings = cur.fetchone()[0]
        print(f"Количество строк в таблице: {count_table_strings}")
        if count_table_strings > 250 and num_items == 2:
            num_strings = 0

        # Дублируем измененные строки num_strings раз
        final_rows = []
        for _ in range(num_strings):
            final_rows.extend(updated_rows)

        # Удаляем старые строки с отрицательными значениями
        delete_query = f"DELETE FROM 'weather_{num_id}' WHERE clothes_type < 0"
        cur.execute(delete_query)

        # Добавляем новые строки в таблицу
        insert_query = f"INSERT INTO 'weather_{num_id}' VALUES ({','.join(['?' for _ in range(len(final_rows[0]))])})"
        cur.executemany(insert_query, final_rows)

        # Сохраняем изменения
        conn.commit()

        print(f"{len(final_rows)} строк успешно добавлено в таблицу 'weather_{num_id}'.")
    else:
        print("Строк с отрицательными значениями в колонке 'clothes_type' не обнаружено.")


def clear_databese_if_not_callback(num_id, conn, cur):
    # Выполняем запрос для удаления строк с отрицательными значениями в столбце 'clothes_type'
    query = f"DELETE FROM 'weather_{num_id}' WHERE clothes_type < 0"
    cur.execute(query)

    # Сохраняем изменения
    conn.commit()

    # Проверим, сколько строк было удалено
    rows_deleted = cur.rowcount

    if rows_deleted > 0:
        print(f"Удалены {rows_deleted} строк с отрицательными значениями в колонке 'clothes_type'.")
    else:
        print("Строки с отрицательными значениями в колонке 'clothes_type' отсутствуют.")


# функция нормализации
def knn_and_rewrite(num_id, x_test):
    # данный порядок не просто так - индекс каждого
    # элемента будет коэффициентом нормализации
    # weather_main_codes = [
    #     'Clear', 'Clouds', 'Drizzle', 'Rain', 'Snow', 'Thunderstorm'
    #     # 'Mist',
    #     # 'Smoke',
    #     # 'Haze',
    #     # 'Dust',
    #     # 'Fog',
    #     # 'Sand',
    #     # 'Dust',
    #     # 'Ash',
    #     # 'Squall',
    #     # 'Tornado'
    # ]
    # x_test[0][0] = weather_main_codes.index(x_test[0][0])
    x_test = x_test.transpose()
    conn_n = sqlite3.connect('../database/weather_outside.sqlite3')
    cur = conn_n.cursor()

    # очистим таблицу от временных данных, на которые пользователь не ответил
    clear_databese_if_not_callback(num_id, conn_n, cur)

    df = pd.read_sql("SELECT * FROM 'weather_%d'" %num_id, conn_n)
    # print(df)
    x_train, y_train = df.iloc[:, :-1], df.iloc[:, -1]
    # print(x_train, y_train)
    df['main'] = df['main'] /5 #normalization
    df['temp'] = (df['temp'] -5)/10
    df['temp_min'] = (df['temp_min'] - 5) / 10
    df['temp_max'] = (df['temp_max'] - 5) / 10
    df['humidity'] = df['humidity']/100
    df['wind_speed'] = df['wind_speed']/20
    df['clouds'] = df['clouds']/100
    # print(df)

    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(x_train, y_train)
    y_res = model.predict(x_test)
    #print(y_res)
    conn_n.commit()
    # cur.execute("SELECT * INTO 'weather_%d' FROM 'weather" %num_id)

    cur.close()
    conn_n.close()

    return clothes_codes[y_res[0]], y_res[0]