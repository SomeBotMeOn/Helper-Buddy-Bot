# модули для работы с env
import os
from dotenv import load_dotenv
import telebot

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env\\.env'))
bot = telebot.TeleBot(os.getenv("TOKEN")) # ссылаемся на токен в файле evn
API_weather = os.getenv("API_W") # ссылаемся на апишник в файле evn