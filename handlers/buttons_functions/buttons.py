from telebot import types

from handlers.classification_functions.classification_news import news
from handlers.weather_functions.weather import show_weather
from bot_instance import bot
from models.classification.rewrite_classif_data import personal_cloth
from models.parser.event_parser.event_parser_file import send_event_news
from models.classification.clothes_response import send_feedback_request

def func_buttons(message):
    # создаем кнопки
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    weather_button = types.KeyboardButton('Погода')
    news_button = types.KeyboardButton('Новости')
    clothes_button = types.KeyboardButton('Одежда')
    events_button = types.KeyboardButton('Мероприятия')
    feedback_button = types.KeyboardButton('Отзыв')
    markup.row(weather_button, news_button)
    markup.row(clothes_button, events_button)
    markup.row(feedback_button)
    bot.send_message(message.chat.id, "Что вы хотите узнать сегодня?", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Погода')
def import_show_weather(message):
    # функция вызывает печать информации о погоде из файла weather.py
    show_weather(message)

@bot.message_handler(func=lambda message: message.text == 'Одежда')
def show_cloth(message):
    # функция вызывает печать подходящей одежды под погоду
    personal_cloth(message)

@bot.message_handler(func=lambda message: message.text == 'Новости')
def show_news(message):
    # функция вызывает печать новостей
    news(message)

@bot.message_handler(func=lambda message: message.text == 'Мероприятия')
def show_events(message):
    # функция вызывает печать мероприятий
    send_event_news(message)

@bot.message_handler(func=lambda message: message.text == 'Отзыв')
def handle_feedback_request(message):
    # функция вызывает отправку сообщения с отзывом
    send_feedback_request(message)

