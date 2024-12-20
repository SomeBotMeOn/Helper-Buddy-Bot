import sqlite3

import telebot
import requests

from utilits.logger import commands_bot
from bot_instance import bot, API_weather
from handlers.buttons_functions.buttons import func_buttons
from database.personal_classif import personal_classification

# Обработка других встроенных команд
def weather(message):
    # функция выводит текущую погоду
    user_id = message.from_user.id
    conn = sqlite3.connect('../database/weather_outside.sqlite3')
    cur = conn.cursor()
    cur.execute("SELECT city FROM users WHERE id=?",
                (user_id,))
    result = cur.fetchone()

    if result:
        city = result[0]
        res_current_weather = requests.get(
            f'https://ru.api.openweathermap.org/data/2.5/weather?q={city}&appid={API_weather}&units=metric&lang=ru'
        )
        bot.reply_to(message, f'Погода в данный момент: {res_current_weather.json()}')
    else:
        bot.reply_to(message, f'Произошла непредвиденная ошибка! Пожалуйста, повторите запрос позднее!')

    cur.close()
    conn.close()

def information(message):
    # Выводит всю информацию о пользователе и чате
    bot.send_message(message.chat.id, message)

def commands(message):
    # функция выводит список команд
    commands_list = '\n'.join(commands_bot)
    bot.send_message(message.chat.id, commands_list)

def ask_user_name(message):
    # Спрашиваем имя пользователя
    ask_name_message = 'Как я могу к Вам обращаться?'
    bot.send_message(message.chat.id, ask_name_message, parse_mode='html')
    bot.register_next_step_handler(message, get_user_name)

def get_user_name(message):
    # Получаем и сохраняем имя пользователя
    name = message.text.strip()
    conn = sqlite3.connect('../database/weather_outside.sqlite3')
    cur = conn.cursor()
    cur.execute('SELECT id FROM person WHERE id = ?',
                (message.from_user.id,))
    if cur.fetchone() is not None:
        # Если пользователь уже есть, обновим его имя
        cur.execute('UPDATE person SET name = ? WHERE id = ?',
                    (name, message.from_user.id))
    else:
        cur.execute('INSERT INTO person (id, name) VALUES (?, ?)',
                    (message.from_user.id, name))
    conn.commit()

    confirmation_message = f"Спасибо, {name}! Ваше имя сохранено."
    bot.send_message(message.chat.id, confirmation_message, parse_mode='html')

    ask_user_city(message)

def ask_user_city(message):
    # Спрашиваем город пользователя
    ask_city_message = 'Теперь, пожалуйста, укажите Ваш город:'
    bot.send_message(message.chat.id, ask_city_message, parse_mode='html')
    bot.register_next_step_handler(message, get_user_city)

def check_city_exists(city_name):
    # Функция проверяет город, введенный пользователем
    url = f"http://ru.api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_weather}"
    response = requests.get(url)

    if response.status_code == 200:
        return True
    else:
        return False

def get_user_city(message):
    # Получаем и сохраняем город пользователя

    city = message.text.strip()

    # Проверяем город на существование
    if check_city_exists(city):
        conn = sqlite3.connect('../database/weather_outside.sqlite3')
        cur = conn.cursor()
        cur.execute('SELECT * FROM person WHERE id = ?',
                    (message.from_user.id,))
        user = cur.fetchone()
        if user:  # Если пользователь существует, обновляем его город
            cur.execute('UPDATE person SET city = ? WHERE id = ?',
                        (city, message.from_user.id))
            confirmation_message = f"Ваш город был обновлен на {city}!"
        else:  # Иначе добавляем нового пользователя с указанным городом
            cur.execute('INSERT INTO person (id, city) VALUES (?, ?)',
                        (message.from_user.id, city))
            confirmation_message = f"Спасибо, Ваш город {city} был успешно добавлен!"
        conn.commit()
        cur.close()
        conn.close()

        bot.send_message(message.chat.id, confirmation_message, parse_mode='html')

        personal_classification(message.from_user.id)

        # ПОСЛЕ СБОРА ВСЕХ ДАННЫХ ОТОБРАЖАЕМ КНОПКИ
        func_buttons(message)

    else:
        error_message = f"К сожалению, Вы указали город с ошибкой, либо такого города не существует! Попробуйте еще раз!"
        msg = bot.send_message(message.chat.id, error_message, parse_mode='html')
        bot.register_next_step_handler(msg, get_user_city)
