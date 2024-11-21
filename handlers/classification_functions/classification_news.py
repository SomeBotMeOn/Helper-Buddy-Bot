from models.parser.news_parser.economic_parser import send_economic_news
from models.parser.news_parser.incident_parser import send_incident_news
from models.parser.news_parser.policy_parser import send_policy_news
from models.parser.news_parser.science_parser import send_science_news
from models.parser.news_parser.society_parser import send_society_news
from models.parser.news_parser.sport_parser import send_sport_news
from bot_instance import bot
from telebot import types

def news(message):
    # функция предлагает пользователю выбрать категорию новостей
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Экономика', callback_data='classif_news_economics')
    btn2 = types.InlineKeyboardButton('Происшествия', callback_data='classif_news_incidents')
    btn3 = types.InlineKeyboardButton('Политика', callback_data='classif_news_politics')
    btn4 = types.InlineKeyboardButton('Наука', callback_data='classif_news_science')
    btn5 = types.InlineKeyboardButton('Общество', callback_data='classif_news_society')
    btn6 = types.InlineKeyboardButton('Спорт', callback_data='classif_news_sport')
    btn7 = types.InlineKeyboardButton('Не смотреть новости', callback_data='classif_news_no_news')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.row(btn5, btn6)
    markup.row(btn7)
    bot.send_message(message.chat.id, "Выберите категорию новостей:", reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: callback.data.startswith('classif_news_'))
def callback_message(callback):
    if callback.data == 'classif_news_economics':
        send_economic_news(callback.message)
    elif callback.data == 'classif_news_incidents':
        send_incident_news(callback.message)
    elif callback.data == 'classif_news_politics':
        send_policy_news(callback.message)
    elif callback.data == 'classif_news_science':
        send_science_news(callback.message)
    elif callback.data == 'classif_news_society':
        send_society_news(callback.message)
    elif callback.data == 'classif_news_sport':
        send_sport_news(callback.message)
    elif callback.data == 'classif_news_no_news':
        bot.send_message(callback.message.chat.id, "Вы выбрали не смотреть новости 🙁")