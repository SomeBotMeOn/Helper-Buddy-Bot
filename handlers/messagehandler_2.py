import sqlite3
import telebot
import requests
import datetime

from pyexpat.errors import messages
from utilits.logger import commands_bot
from telebot import types
from bot_instance import bot, API_weather
from utilits.assets import stickers, emoji, icon_to_emoji
from handlers.weather import show_weather

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
def import_show_weather(message):
    # функция вызывает печать информации о погоде из файла weather.py
    show_weather(message)




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