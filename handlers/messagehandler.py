from bot_instance import bot
from utilits.assets import stickers, emoji

# функция обработки сообщений от пользователя
def info(message):
    if message.text.lower() == 'привет':
        #bot.send_sticker(message.chat.id, sticker['hi_sticker'])
        bot.send_message(message.chat.id, emoji['hi_emoji'])
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}') # ответ на сообщение

