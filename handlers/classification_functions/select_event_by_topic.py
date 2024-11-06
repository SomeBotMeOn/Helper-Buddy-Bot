from telebot import types
from bot_instance import bot

event_data = {}
event_counter = 0  # Глобальный счётчик для уникальных идентификаторов событий

def select_event(message, events_array):
    # Функция предлагает пользователю выбрать событие из списка

    global event_counter

    # Создаем сообщение с названиями событий
    message_text = f"🎭 Яндекс Афиша: {events_array[0]['topic']}\n\n"
    for i, event_item in enumerate(events_array, start=1):
        message_text += f"📅 Событие {i}: {event_item['title']}\n\n"
    markup = types.InlineKeyboardMarkup()

    buttons = []

    for i, event_item in enumerate(events_array, start=1):
        event_id = event_counter
        event_counter += 1
        # Сохраняем событие в глобальном словаре с уникальным идентификатором
        event_data[str(event_id)] = event_item
        # В callback_data используем уникальный идентификатор события
        button = types.InlineKeyboardButton(
            f"Событие {i}", callback_data=f'event_{event_id}'
        )
        buttons.append(button)

    # Добавляем кнопки в разметку
    markup.row(buttons[0], buttons[1])
    markup.row(buttons[2], buttons[3])
    markup.row(buttons[4])

    # Отправляем сообщение с разметкой
    bot.send_message(
        message.chat.id,
        message_text,
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda callback: callback.data.startswith('event_'))
def callback_event(callback):
    # Обработка нажатия на кнопку события
    event_id = callback.data.split('_')[1]
    event_item = event_data.get(event_id)
    if event_item:
        # Отправляем ссылку на событие
        bot.send_message(
            callback.from_user.id,
            f"Ссылка на событие: {event_item['link']}",
        )
    else:
        # Сообщаем, что событие не найдено или ссылка устарела
        bot.send_message(
            callback.from_user.id,
            "Событие не найдено или ссылка устарела. Попробуйте еще раз!",
        )