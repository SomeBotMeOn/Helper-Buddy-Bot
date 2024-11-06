import requests
from bs4 import BeautifulSoup
import urllib.parse
from bot_instance import bot
from handlers.classification_functions.select_event_by_topic import select_event

def send_event_news(message):
    """
    Эта функция получает последние события с указанного URL и отправляет
    массив из первых 5 событий вместе с их ссылками в функцию select_event().
    """
    url = 'https://afisha.yandex.ru/moscow/selections/nearest-events'  # URL страницы с событиями
    base_url = 'https://afisha.yandex.ru'  # Базовый URL для формирования полных ссылок

    # Заголовки для имитации браузера
    headers = {'accept': '*/*',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
              }

    # Отправляем GET-запрос на страницу
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'  # Устанавливаем кодировку

    # Проверяем успешность запроса
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим все элементы с событиями
        events = soup.find_all("div", class_="event events-list__item yandex-sans")
        events_url = soup.find_all("div", class_="Badges-njdnt8-7 eSHAvL")

        print(events, events_url)

        # Проверяем, что найдены события
        if events and events_url:
            events_array = []
            # Извлекаем первые 5 событий
            for event, event_url in zip(events[:5], events_url[:5]):
                name_tag = event.find("div", class_="Root-fq4hbj-4 iFrhLC").find('h2')
                link_tag = event_url.find('a')
                if name_tag and link_tag:
                    name = name_tag.get_text(strip=True)
                    link = link_tag['href']
                    # Преобразуем относительную ссылку в абсолютную
                    absolute_link = urllib.parse.urljoin(base_url, link)
                    # Добавляем событие в массив
                    events_array.append({'topic': 'События', 'title': name, 'link': absolute_link})
            # Вызываем функцию select_event() с массивом событий
            select_event(message, events_array)
        else:
            bot.send_message(message.chat.id, "На данный момент актуальных событий не найдено.")
    else:
        bot.send_message(message.chat.id, f"Ошибка при подключении к сайту: {response.status_code}")
