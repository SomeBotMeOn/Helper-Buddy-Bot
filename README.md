﻿# Helper-Buddy-Bot

Наш телеграм-бот сделает всё, чтобы вы чувствовали себя комфортно в любую погоду и всегда знали, как можно провести время, а также не упустили интересные события вокруг вас 😊

Проект разработан для пользователей из разных городов России для лёгкого и быстрого доступа к новостям, мероприятиям и погоде.

## Цель

Создание телеграм-бота, определяющего погоду, наилучшее сочетание в одежде, список актуальных мероприятий и новостей.

## Задачи бота

1. **Предсказывать погоду.**

2. **Предоставлять пользователю лучшее сочетание одежды** для погоды на данный момент, основываясь на его предпочтениях и личном ощущении той или иной погоды.

3. **Давать возможность пользователю скорректировать рекомендации в одежде.** Исправлять в будущем предсказания одежды, если пользователя не устроил результат.

4. **Выводить самые актуальные на данный момент новости** по запросу пользователя.

5. **Выводить мероприятия** по запросу пользователя.

## Архитектура проекта

### 1. config (конфигурация)

- `__init__.py`
- `main.py` – тело бота

### 2. database (база данных)

- `__init__.py`
- `personal_classif.py` – создание личной таблицы пользователя

### 3. handlers (отвечает за обработку сообщений)

#### 3.1. buttons_functions (создание кнопок главного меню)

- `__init__.py`
- `buttons.py` – вызов функций для печати при нажатии определённых кнопок из меню

#### 3.2. classification_functions (обработка мероприятий и новостей при вызове кнопки)

- `__init__.py`
- `classification_news.py` – функция для печати новостей
- `select_event_by_topic.py` – функция для печати событий
- `select_new_by_topic.py` – функции для выбора конкретных новостей/мероприятий, выбранных пользователем

#### 3.3. user_handlers

- `__init__.py`
- `messagehandler.py` – обработка сообщения от пользователя
- `messagehandler_2.py` – обработка прочих встроенных команд
- `starthandler.py` – для хранения информации о пользователе и чате

#### 3.4. weather_functions

- `__init__.py`
- `weather.py` – получение текущей погоды

### 4. models (основные действия бота кроме погоды)

#### 4.1. classification (реализация выбора одежды)

- `__init__.py`
- `clothes_response.py` – обработка комментария пользователя об одежде
- `rewrite_classif_data.py` – подбирает пользователю одежду по базе данных

#### 4.2. parser (реализация парсеров)

##### 4.2.1. event_parser (парсер мероприятий)

- `__init__.py`
- `event_parser_file.py` – парсер мероприятий

##### 4.2.2. news_parser (сборник парсеров новостей)

- `__init__.py`
- `economic_parser.py` – парсер новостей экономики
- `incident_parser.py` – парсер новостей происшествий
- `policy_parser.py` – парсер новостей политики
- `science_parser.py` – парсер новостей науки
- `society_parser.py` – парсер новостей категории «общество»
- `sport_parser.py` – парсер новостей спорта

### 5. utilits

- `__init__.py`
- `assets.py` – стикеры, смайлики
- `logger.py` – команды бота
- `utilits_funcs.py` – вызов города пользователя из базы данных

### 6. .gitignore

- Для игнорирования Git некоторыми файлами

### 7. README.md

- Документация

### 8. bot_instance.py

- Модули для работы с `env`

*Примечание: `__init__.py` обозначает, что каталог является Python-пакетом. Инициализирует пакеты: выполняет код при первом импорте пакета.*

### Требования для запуска

- Python 3.7+
- Установленные библиотеки из requirements.txt
- Токен Telegram-бота

### Инструкция для запуска

#### Шаг 1: Установка Python

Если у вас еще не установлен Python 3.7 или выше, скачайте и установите его с официального сайта python.org (https://www.python.org/downloads/).

#### Шаг 2: Клонирование или скачивание проекта

1. Клонирование репозитория: git clone https://github.com/SomeBotMeOn/Helper-Buddy-Bot.git
2. Скачивание архива:

   Если у вас есть архив с проектом, распакуйте его в удобное место на вашем компьютере.

#### Шаг 3: Установка зависимостей

1. Откройте терминал и перейдите в директорию с проектом:    cd *путь_к_директории_проекта*
2. Создайте виртуальное окружение (рекомендуется):    python -m venv venv
3. Активируйте виртуальное окружение:

   - На Windows: venv\Scripts\activate
   - На macOS/Linux:source venv/bin/activate

4. Установите необходимые библиотеки: pip install -r requirements.txt

#### Шаг 4: Получение токена Telegram-бота

1. Откройте Telegram и найдите бота @BotFather (https://t.me/BotFather).
2. Создайте нового бота:

   Отправьте команду /newbot и следуйте инструкциям для создания бота. Вам будет предложено указать имя и юзернейм бота.

3. Получите токен

#### Шаг 5: Настройка бота

1. Создайте файл конфигурации:

   В корневой директории проекта создайте файл .env или используйте существующий файл настроек (например, config.py), в зависимости от структуры вашего проекта.

2. Добавьте токен в файл конфигурации:

   - Если используете .env файл, добавьте строку: TELEGRAM_BOT_TOKEN=ваш_токен_бота
   - Если используете config.py, добавьте: TELEGRAM_BOT_TOKEN = 'ваш_токен_бота'

#### Шаг 6: Запуск бота

1. Убедитесь, что вы находитесь в виртуальном окружении (если создавали его ранее).
2. Запустите бота

# Запуск бота пользователем

При первом запуске бота на экране пользователя появляется команда «СТАРТ». Бот приветствует пользователя, используя в качестве обращения ник в Telegram. Далее бот запрашивает, как пользователь хотел бы, чтобы к нему обращались. После этого бот сохраняет пользователя в базу данных с базовым набором одежды. Затем бот запрашивает город — это необходимо для предсказания погоды и выбора актуальных мероприятий. Далее бот спрашивает, что бы хотелось узнать пользователю в данный момент. У пользователя в меню есть кнопки:

1. ПОГОДА — отправляет погоду на данный момент в регионе.
2. МЕРОПРИЯТИЯ — выводит 5 самых популярных мероприятий. Пользователь может узнать подробнее о каждом из них, нажав на мероприятие.
3. НОВОСТИ — бот запрашивает категории новостей, которые хотел бы увидеть пользователь (экономика, происшествия, политика, наука, общество, спорт). После выбора категории предоставляются 5 самых актуальных новостей. При нажатии на новость бот отправляет ссылку на неё.
4. ОДЕЖДА — бот рекомендует пользователю одежду, соответствующую погоде.
5. ОТЗЫВ — в случае неудовлетворения пользователя одеждой, которую порекомендовал бот, пользователь может отправить свой отзыв:

   - "Мне было очень жарко / надел одежду гораздо легче"
   - "В этом было жарковато / оделся чуть-чуть полегче"
   - "Да, это подходило под погоду"
   - "В этом было прохладно / оделся чуть-чуть теплее"
   - "Мне было очень холодно / надел одежду гораздо теплее"

   Далее бот благодарит пользователя за отзыв.

## Прочие доступные команды

- /start — приветствие с именем и фамилией
- /information — информация о чате и пользователе
- привет — эмодзи приветствия (👋)
- id — ID пользователя
- /site_weather, /website_weather, /сайт_погода — ссылка на сайт с погодой
- /users — выводит всех пользователей