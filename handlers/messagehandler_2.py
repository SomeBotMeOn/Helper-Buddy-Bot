import sqlite3
import telebot
import requests
import datetime

from pyexpat.errors import messages
from utilits.logger import commands_bot
from telebot import types
from bot_instance import bot, API_weather
from utilits.assets import stickers, emoji, icon_to_emoji

# Обработка других встроенных команд
def weather(message):
    # функция выводит текущую погоду
    res_current_weather = requests.get(f'https://ru.api.openweathermap.org/data/2.5/weather?q=Moscow&appid={API_weather}&units=metric&lang=ru')
    bot.reply_to(message, f'Погода в данный момент: {res_current_weather.json()}')

def information(message):
    # Выводит всю информацию о пользователе и чате
    bot.send_message(message.chat.id, message)

def site_with_weather(message):
    # функция отправляет пользователя на сайт с погодой
    webbrowser.open('https://openweathermap.org/weathermap')

def commands(message):
    # функция выводит список команд
    commands_list = '\n'.join(commands_bot)
    bot.send_message(message.chat.id, commands_list)

def user_name(message):
    name = message.text.strip()

    conn = sqlite3.connect('../database/users_db.sql')
    cur = conn.cursor()

    cur.execute('INSERT INTO users (id, name) VALUES (?, ?)', (message.from_user.id, name))

    conn.commit()
    cur.close()
    conn.close()

    # Отправляем подтверждение пользователю
    confirmation_message = f"Спасибо, {name}! Ваше имя сохранено."
    bot.send_message(message.chat.id, confirmation_message, parse_mode='html')

    # ПЕРЕСТАВИТЬ BUTTON ТАК, ЧТОБЫ ОНИ ПОЯВЛЯЛИСЬ ПОСЛЕ ВВОДА ПОЛЬЗОВАТЕЛЕМ ВСЕЙ ИНФОРМАЦИИ
    buttons(message)

def buttons(message):
    # создаем кнопки
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    weather_button = types.KeyboardButton('Погода')
    news_button = types.KeyboardButton('Новости')
    markup.row(weather_button, news_button)
    bot.send_message(message.chat.id, "Что вы хотите узнать сегодня?", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Погода')
def show_weather(message):
    # Выводим погоду
    res_current_weather = requests.get(
        f'https://ru.api.openweathermap.org/data/2.5/weather?q=Moscow&appid={API_weather}&units=metric&lang=ru'
    )
    weather_data = res_current_weather.json()

    city = weather_data['name']
    temp = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    weather_description = weather_data['weather'][0]['description']
    wind_speed = weather_data['wind']['speed']
    visibility = weather_data['visibility']
    humidity = weather_data['main']['humidity']
    sunrise_timestamp = datetime.datetime.fromtimestamp(weather_data["sys"]["sunrise"])
    sunset_timestamp = datetime.datetime.fromtimestamp(weather_data["sys"]["sunset"])
    pressure = weather_data['main']['pressure']

    weather_icon = weather_data['weather'][0]['icon']
    weather_emoji = icon_to_emoji.get(weather_icon, "")

    message_lines = []
    message_lines.append(f"Погода в городе {city}: {temp} °C {weather_emoji}")
    message_lines.append(f"Ощущается как {feels_like} °C")

    # Вывод текущего состояния погоды с описанием и эмодзи
    message_lines.append(f"{weather_description.capitalize()} {weather_emoji}")

    # Вывод давления
    message_lines.append(f'Давление: {pressure} мм.рт.ст.')

    # Проверка на сильный ветер
    if wind_speed > 5:
        message_lines.append(f"Ожидается сильный ветер: {wind_speed} м/c 💨")

    # Проверка на влажность
    if humidity <= 50:
        message_lines.append(f'Влажность: {humidity}%, пониженная влажность 🌵')
    elif humidity >= 70:
        message_lines.append(f'Влажность: {humidity}%, повышенная влажность 💦')

    # Проверка на критическую температуру
    if temp >= 30:
        message_lines.append(f'❗ Высокая температура: {temp} 🥵')
    elif temp <= -25:
        message_lines.append(f'❗ Низкая температура: {temp} 🥶')

    # Проверка на видимость
    if visibility < 500:
        message_lines.append(f"⚠️ Видимость сильно ограничена: {visibility} м ⚠️")
    elif visibility < 1000:
        message_lines.append(f"⚠️ Видимость ограничена: {visibility} м ⚠️")

    # Вывод заката и восхода солнца
    sunrise_formatted = sunrise_timestamp.strftime("%H:%M")
    sunset_formatted = sunset_timestamp.strftime("%H:%M")
    message_lines.append('\n')
    message_lines.append(f"🌅 Восход: {sunrise_formatted}")
    message_lines.append(f"🌇 Закат: {sunset_formatted}")

    # В ДРУГОМ https://openweathermap.org/forecast5 (Forecast) можно выводить прогноз на 4 часа


    final_message = '\n'.join(message_lines)

    bot.send_message(message.chat.id, final_message)



#  УДАЛИТЬ ПОТОМ, ТАК КАК ФУНКЦИЯ ВЫВОДИТ ВСЮ БД

def print_all_users(message):
    # функция выводит всех пользователей
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot.send_message(message.chat.id, 'Вы можете обновить список, нажав на кнопку ниже.', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('../database/users_db.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    info = ''
    for el in users:
        info += (f'Id: {el[0]}, Имя: {el[1]}\n')

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)