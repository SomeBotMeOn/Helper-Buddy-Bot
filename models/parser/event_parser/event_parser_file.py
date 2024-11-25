import requests
from bs4 import BeautifulSoup
import urllib.parse
from bot_instance import bot
from handlers.classification_functions.select_event_by_topic import select_event

def send_event_news(message):
    """
    Эта функция получает последние события с указанного URL и отправляет
    массив из первых 5 событий вместе с их ссылками и датами в функцию select_event().
    """
    url = 'https://afisha.yandex.ru/moscow/selections/nearest-events'  # URL страницы с событиями
    base_url = 'https://afisha.yandex.ru'  # Базовый URL для формирования полных ссылок

    # Заголовки для имитации браузера
    headers = {
        'User-Agent': urllib.parse.quote('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, как Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.3')
    }

    # Отправляем GET-запрос на страницу
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'  # Устанавливаем кодировку

    # Проверяем успешность запроса
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')

        # Находим все элементы с событиями
        events = soup.find_all("div", class_="event events-list__item yandex-sans")
        events_url = soup.find_all("div", class_="Badges-njdnt8-7 eSHAvL")

        # Проверяем, что найдены события
        if events and events_url:
            events_array = []
            # Извлекаем первые 5 событий
            for event, event_url in zip(events[:5], events_url[:5]):
                # Извлечение названия события
                name_tag = event.find("div", class_="Root-fq4hbj-4 iFrhLC").find('h2')
                # Извлечение даты события
                # Предполагается, что дата находится внутри тега <ul><li> внутри блока event
                date_tag = event.find('ul')
                if date_tag:
                    date_text = date_tag.find('li').get_text(strip=True)
                else:
                    date_text = "Дата не указана"

                # Извлечение ссылки на событие
                link_tag = event_url.find('a')
                if name_tag and link_tag:
                    name = name_tag.get_text(strip=True)
                    link = link_tag.get('href')
                    if link:
                        # Преобразуем относительную ссылку в абсолютную
                        absolute_link = urllib.parse.urljoin(base_url, link)
                    else:
                        absolute_link = "Ссылка не указана"

                    # Добавляем событие в массив с датой
                    events_array.append({
                        'topic': 'События',
                        'title': name,
                        'link': absolute_link,
                        'date': date_text
                    })

            if events_array:
                # Вызываем функцию select_event() с массивом событий
                select_event(message, events_array)
            else:
                bot.send_message(message.chat.id, "На данный момент актуальных событий не найдено.")
        else:
            bot.send_message(message.chat.id, "На данный момент актуальных событий не найдено.")
    else:
        bot.send_message(message.chat.id, f"Ошибка при подключении к сайту: {response.status_code}")