from models.parser.economic_parser import send_economic_news
from models.parser.incident_parser import send_incident_news
from models.parser.policy_parser import send_policy_news
from models.parser.science_parser import send_science_news
from models.parser.society_parser import send_society_news
from models.parser.sport_parser import send_sport_news
from bot_instance import bot
from telebot import types

def news(message):
    # функция предлагает пользователю выбрать категорию новостей
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Экономика', callback_data='economics')
    btn2 = types.InlineKeyboardButton('Происшествия', callback_data='incidents')
    btn3 = types.InlineKeyboardButton('Политика', callback_data='politics')
    btn4 = types.InlineKeyboardButton('Наука', callback_data='science')
    btn5 = types.InlineKeyboardButton('Общество', callback_data='society')
    btn6 = types.InlineKeyboardButton('Спорт', callback_data='sport')
    btn7 = types.InlineKeyboardButton('Не смотреть новости', callback_data='no_news')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.row(btn5, btn6)
    markup.row(btn7)
    bot.send_message(message.chat.id, "Выберите категорию новостей:", reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'economics':
        send_economic_news(callback.message)
    elif callback.data == 'incidents':
        send_incident_news(callback.message)
    elif callback.data == 'politics':
        send_policy_news(callback.message)
    elif callback.data == 'science':
        send_science_news(callback.message)
    elif callback.data == 'society':
        send_society_news(callback.message)
    elif callback.data == 'sport':
        send_sport_news(callback.message)
    elif callback.data == 'no_news':
        bot.send_message(callback.message.chat.id, "Вы выбрали не смотреть новости 🙁")