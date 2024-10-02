# заносим команды в @BotFather (бот в тг)
commands_bot = [
    '/start', # привет имя фамилия
    '/information', # инфа о чате и пользователе
    'привет', # эмодзи привет (ладошка)
    'id' # id пользователя
    '/site_weather, /website_weather, /сайт_погода' # отправляет пользователя на сайт
]

def commands(message):
    # функция выводит список команд
    commands_list = '\n'.join(commands_bot)
    bot.send_message(message.chat.id, commands_list)