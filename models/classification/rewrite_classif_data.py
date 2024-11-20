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
clothes_codes = [
    'свитер/худи, зимняя куртка/пуховик, шапка, шарф, перчатки',
    "лонгслив/легкий свитер, зимняя куртка/пуховик, шапка, шарф",
    "свитер/худи, пальто/куртка, шапка, шарф",
    "лонгслив/легкий свитер, пальто/куртка",
    "свитер/худи, ветровка/плащ",
    "майка/футболка/лонгслив, ветровка/плащ",
    "майка/футболка/лонгслив, свитер/худи",
    "майка/футболка/лонгслив, кофта/пиджак",
    "свитер/худи",
    "футболка/лонгслив/легкий свитер",
    "майка/футболка"
]


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