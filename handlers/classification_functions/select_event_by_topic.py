from telebot import types
from bot_instance import bot

# Глобальный словарь для хранения информации о событиях
event_data = {}
event_counter = 0  # Глобальный счётчик для уникальных идентификаторов событий


def select_event(message, events_array):
    """
    Эта функция предлагает пользователю выбрать событие из списка,
    отображая название и дату каждого события.
    """
    global event_counter

    if not events_array:
        bot.send_message(message.chat.id, "На данный момент актуальных событий не найдено.")
        return

    # Начинаем формировать текст сообщения с темой
    message_text = f"🎭 Яндекс Афиша: {events_array[0]['topic']}\n\n"

    # Добавляем информацию о каждом событии: номер, название и дату
    for i, event_item in enumerate(events_array, start=1):
        message_text += (
            f"📅 <b>Событие {i}:</b> {event_item['title']}\n"
            f"🗓 <b>Дата:</b> {event_item['date']}\n\n"
        )

    # Создаём разметку для инлайн-кнопок
    markup = types.InlineKeyboardMarkup()
    buttons = []

    for i, event_item in enumerate(events_array, start=1):
        event_id = event_counter
        event_counter += 1
        # Сохраняем событие в глобальном словаре с уникальным идентификатором
        event_data[str(event_id)] = event_item
        # В callback_data используем уникальный идентификатор события
        button = types.InlineKeyboardButton(
            f"Подробнее о событии {i}",
            callback_data=f'event_{event_id}'
        )
        buttons.append(button)

    # Размещаем кнопки по 2 в ряд. Если количество кнопок нечётное, последняя будет одна.
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            markup.add(buttons[i], buttons[i + 1])
        else:
            markup.add(buttons[i])

    # Отправляем сообщение с разметкой
    bot.send_message(
        message.chat.id,
        message_text,
        parse_mode='HTML',  # Позволяет использовать HTML-теги для форматирования
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda callback: callback.data.startswith('event_'))
def callback_event(callback):
    """
    Обработка нажатия на кнопку события.
    Отправляет пользователю подробную информацию о выбранном событии.
    """
    event_id = callback.data.split('_')[1]
    event_item = event_data.get(event_id)

    if event_item:
        # Формируем подробное сообщение о событии
        detailed_message = (
            f"🎭 <b>{event_item['title']}</b>\n"
            f"🗓 <b>Дата:</b> {event_item['date']}\n"
            f"🔗 <b>Ссылка на событие:</b> {event_item['link']}"
        )
        bot.send_message(
            callback.from_user.id,
            detailed_message,
            parse_mode='HTML',
            disable_web_page_preview=True  # Отключает предпросмотр ссылок для чистого вида
        )
    else:
        # Сообщаем, что событие не найдено или ссылка устарела
        bot.send_message(
            callback.from_user.id,
            "❌ Событие не найдено или ссылка устарела. Попробуйте еще раз!",
        )