from telebot import types
from bot_instance import bot

def send_feedback_request(message):
    """
    Отправляет сообщение с вопросом о полезности совета по одежде и кнопками для ответа.
    """
    feedback_message = "Был ли мой совет об одежде полезен? Если вы надели другую одежду, всё равно ответьте на вопрос, это поможет мне подстроиться под ваше ощущение погоды."
    markup = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton("Мне было очень жарко/надел одежду гораздо легче", callback_data='feedback_0'),
        types.InlineKeyboardButton("В этом было жарковато/оделся чуть-чуть полегче", callback_data='feedback_1'),
        types.InlineKeyboardButton("Да, это подходило под погоду", callback_data='feedback_2'),
        types.InlineKeyboardButton("В этом было прохладно/оделся чуть-чуть теплее", callback_data='feedback_3'),
        types.InlineKeyboardButton("Мне было очень холодно/надел одежду гораздо теплее", callback_data='feedback_4')
    ]
    for button in buttons:
        markup.add(button)
    bot.send_message(message.chat.id, feedback_message, reply_markup=markup)

