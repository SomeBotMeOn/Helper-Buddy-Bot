import requests
from bs4 import BeautifulSoup
import urllib.parse
from bot_instance import bot
from handlers.classification_functions.select_event_by_topic import select_event
from cachetools import TTLCache, cached
from functools import wraps
import time

# Создаём кэш с временем жизни 10 минут и максимальным объёмом 100 записей
cache = TTLCache(maxsize=100, ttl=600)

# Декоратор для ограничения частоты вызовов функции
def rate_limit(max_calls, period):
    lock = {}
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            calls = lock.get(func, [])
            calls = [call for call in calls if call > now - period]
            if len(calls) >= max_calls:
                sleep_time = period - (now - calls[0])
                time.sleep(sleep_time)
                calls = calls[1:]
            calls.append(time.time())
            lock[func] = calls
            return func(*args, **kwargs)
        return wrapper
    return decorator

@cached(cache)
@rate_limit(max_calls=1, period=60)  # Ограничение: не более 1 запроса в минуту
def fetch_events():
    url = 'https://afisha.yandex.ru/moscow/selections/nearest-events'  # URL страницы с событиями
    base_url = 'https://afisha.yandex.ru'  # Базовый URL для формирования полных ссылок

    headers = {
        'accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        events = soup.find_all("div", class_="event events-list__item yandex-sans")
        events_url = soup.find_all("div", class_="Badges-njdnt8-7 eSHAvL")

        if events and events_url:
            events_array = []
            for event, event_url in zip(events[:5], events_url[:5]):
                name_tag = event.find("div", class_="Root-fq4hbj-4 iFrhLC").find('h2')
                date_tag = event.find('ul')
                date_text = date_tag.find('li').get_text(strip=True) if date_tag else "Дата не указана"

                link_tag = event_url.find('a')
                if name_tag and link_tag:
                    name = name_tag.get_text(strip=True)
                    link = link_tag.get('href')
                    absolute_link = urllib.parse.urljoin(base_url, link) if link else "Ссылка не указана"

                    events_array.append({
                        'topic': 'События',
                        'title': name,
                        'link': absolute_link,
                        'date': date_text
                    })

            return events_array
    return None

def send_event_news(message):
    events_array = fetch_events()
    if events_array:
        select_event(message, events_array)
    else:
        bot.send_message(message.chat.id, "На данный момент актуальных событий не найдено или произошла ошибка при загрузке.")

