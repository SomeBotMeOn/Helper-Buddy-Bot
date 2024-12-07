from telebot import types
from bot_instance import bot
from models.classification.rewrite_classif_data import processing_callback_results

def send_feedback_request(message):
    feedback_message = (
        "Был ли мой совет об одежде полезен? Если вы надели другую одежду, "
        "всё равно ответьте на вопрос, это поможет мне подстроиться под ваше ощущение погоды."
    )

    markup = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton(
            "Мне было очень жарко/надел одежду гораздо легче 🥵", callback_data='0'),
        types.InlineKeyboardButton(
            "В этом было жарковато/оделся чуть-чуть полегче 😩", callback_data='1'),
        types.InlineKeyboardButton(
            "Да, это подходило под погоду 😌", callback_data='2'),
        types.InlineKeyboardButton(
            "В этом было прохладно/оделся чуть-чуть теплее 😬", callback_data='3'),
        types.InlineKeyboardButton(
            "Мне было очень холодно/надел одежду гораздо теплее 🥶", callback_data='4')
    ]

    for button in buttons:
        markup.add(button)
    bot.send_message(message.chat.id, feedback_message, reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: callback.data in ['0', '1', '2', '3', '4'])
def handle_feedback_response(callback):
    try:
        bot.answer_callback_query(callback_query_id=callback.id)
        feedback_value = callback.data

        if feedback_value == '0':
            response = "Спасибо за ваш отзыв! Постараюсь учесть, что вам было слишком жарко."
        elif feedback_value == '1':
            response = "Спасибо! Я учту, что было жарковато."
        elif feedback_value == '2':
            response = "Рад слышать, что мой совет оказался полезным!"
        elif feedback_value == '3':
            response = "Спасибо за обратную связь! Учту, что было прохладно."
        elif feedback_value == '4':
            response = "Спасибо! Постараюсь советовать более теплую одежду."
        else:
            response = "Спасибо за ваш отзыв!"

        bot.send_message(callback.message.chat.id, response)

        processing_callback_results(callback.message.chat.id, int(feedback_value))

    except Exception as e:
        print(f'An error occurred: {e}')