from telebot import types
from bot_instance import bot

news_data = {}
news_counter = 0  # Глобальный счётчик для уникальных идентификаторов новостей

def select_new(message, news_array):
    # функция предлагает пользователю выбрать новость из списка

    global news_counter

    # Создаем сообщение с заголовками новостей
    message_text = f"📰 РИА Новости: {news_array[0]['topic']}\n\n"
    for i, news_item in enumerate(news_array, start=1):
        message_text += f"📢 Новость {i}: {news_item['title']}\n\n"
    markup = types.InlineKeyboardMarkup()

    buttons = []

    for i, news_item in enumerate(news_array, start=1):
        news_id = news_counter
        news_counter += 1
        # Сохраняем новость в глобальном словаре с уникальным идентификатором
        news_data[str(news_id)] = news_item
        # В callback_data используем уникальный идентификатор новости
        button = types.InlineKeyboardButton(
            f"Новость {i}", callback_data=f'news_{news_id}'
        )
        buttons.append(button)

    markup.row(buttons[0], buttons[1])
    markup.row(buttons[2], buttons[3])
    markup.row(buttons[4])

    bot.send_message(
        message.chat.id,
        message_text,
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda callback: callback.data.startswith('news_'))
def callback_message(callback):
    news_id = callback.data.split('_')[1]
    news_item = news_data.get(news_id)
    if news_item:
        bot.send_message(
            callback.from_user.id,
            f"Ссылка на новость: {news_item['link']}",
        )
    else:
        bot.send_message(
            callback.from_user.id,
            "Новость не найдена или ссылка устарела. Попробуйте еще раз!",
        )