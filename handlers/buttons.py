from telebot import types

from handlers.weather import show_weather
from bot_instance import bot

def func_buttons(message):
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