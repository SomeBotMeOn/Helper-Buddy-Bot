# Для обработки команды старт

from handlers.user_handlers.messagehandler_2 import ask_user_name
from bot_instance import bot


def main(message):
    # Хранит информацию про пользователя и чат
    first_name = message.from_user.first_name if message.from_user.first_name else 'Незнакомец'
    last_name = message.from_user.last_name if message.from_user.last_name else ''

    greeting_message = (f'<b>Привет, {first_name} {last_name}!</b>\n'
                        'Я телеграм-бот, который может помочь Вам узнать '
                        'погоду в данный момент и как она ощущается лично для Вас, '
                        'а также определиться куда сегодня пойти.')
    bot.send_message(message.chat.id, greeting_message, parse_mode='html')

    ask_user_name(message)
