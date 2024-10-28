import requests
from bs4 import BeautifulSoup
import urllib.parse
from bot_instance import bot
from handlers.classification_functions.select_new_by_topic import select_new

def send_science_news(message):
    """
    Эта функция получает последние новости о науке с указанного URL и отправляет
    массив из первых 5 заголовков новостей вместе с их ссылками в функцию select_new().
    """
    url = 'https://ria.ru/science/'  # URL страницы с новостями науки
    base_url = 'https://ria.ru'  # Базовый URL для формирования полных ссылок

    # Заголовки для имитации браузера
    headers = {
        'User-Agent': urllib.parse.quote('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.3')
    }

    # Отправляем GET-запрос на страницу
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'  # Устанавливаем кодировку

    # Проверяем успешность запроса
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим все элементы с новостями
        news_items = soup.find_all('div', class_='list-item')

        # Проверяем, что найдены новости
        if news_items:
            news_array = []
            # Извлекаем первые 5 новостей
            for news in news_items[:5]:
                title_tag = news.find('a', class_='list-item__title')
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    link = title_tag['href']
                    # Преобразуем относительную ссылку в абсолютную
                    absolute_link = urllib.parse.urljoin(base_url, link)
                    # Добавляем новость в массив
                    news_array.append({'topic': 'Наука', 'title': title, 'link': absolute_link})
            # Вызываем функцию select_new() с массивом новостей
            select_new(message, news_array)
        else:
            bot.send_message(message.chat.id, "На данный момент актуальных новостей по этой категории не найдено.")
    else:
        bot.send_message(message.chat.id, f"Ошибка при подключении к сайту: {response.status_code}")