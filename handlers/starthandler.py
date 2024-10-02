# Для обработки команды старт
from config.bot_instance import bot

def main(message):
    # Хранит информацию про пользователя и чат
    first_name = message.from_user.first_name if message.from_user.first_name else 'Незнакомец'
    last_name = message.from_user.last_name if message.from_user.last_name else ''
    start_message = f'<b>Привет, {first_name} {last_name}!</b>'
    bot.send_message(message.chat.id, start_message, parse_mode='html') # метод отправляет сообщения в текущий чат
    # parse_mode='html' - позволяет работать с сообщениям, как с html