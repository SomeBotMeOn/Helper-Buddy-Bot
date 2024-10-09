import telebot
import requests
import datetime
import sqlite3

from bot_instance import bot, API_weather
from utilits.assets import icon_to_emoji, precip_dict

def get_current_weather(city):
    """Получает текущую погоду для указанного города"""
    res = requests.get(
        f'https://ru.api.openweathermap.org/data/2.5/weather?q={city}&appid={API_weather}&units=metric&lang=ru'
    )
    return res.json()


def get_forecast_weather(city):
    """Получает прогноз погоды на 5 дней с шагом 3 часа для указанного города"""
    res = requests.get(
        f'https://ru.api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_weather}&units=metric&lang=ru'
    )
    return res.json()


def format_current_weather(weather_data):
    """Форматирует данные текущей погоды в текстовое сообщение"""
    city = weather_data['name']
    temp = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    weather_description = weather_data['weather'][0]['description']
    wind_speed = weather_data['wind']['speed']
    visibility = weather_data['visibility']
    humidity = weather_data['main']['humidity']
    pressure = weather_data['main']['pressure']

    sunrise_timestamp = datetime.datetime.fromtimestamp(weather_data["sys"]["sunrise"])
    sunset_timestamp = datetime.datetime.fromtimestamp(weather_data["sys"]["sunset"])

    weather_icon = weather_data['weather'][0]['icon']
    weather_emoji = icon_to_emoji.get(weather_icon, "")

    message_lines = []
    message_lines.append(f"Погода в городе {city}: {temp} °C {weather_emoji}")
    message_lines.append(f"Ощущается как {feels_like} °C")

    # Вывод текущего состояния погоды с описанием и эмодзи
    message_lines.append(f"{weather_description.capitalize()} {weather_emoji}")

    # Вывод давления
    message_lines.append(f'Давление: {pressure} мм.рт.ст.')

    # Проверка на влажность
    if humidity <= 50:
        message_lines.append(f'Влажность: {humidity}%, пониженная 🌵')
    elif humidity >= 70:
        message_lines.append(f'Влажность: {humidity}%, повышенная 💦')

    # Проверка на сильный ветер
    if wind_speed > 5:
        message_lines.append(f"Ожидается сильный ветер: {wind_speed} м/c 💨")

    # Проверка на критическую температуру
    if temp >= 30:
        message_lines.append(f'❗️ Высокая температура: {temp} °C 🥵')
    elif temp <= -25:
        message_lines.append(f'❗️ Низкая температура: {temp} °C 🥶')

    # Проверка на видимость
    if visibility < 500:
        message_lines.append(f"⚠️ Видимость сильно ограничена: {visibility} м ⚠️")
    elif 500 <= visibility < 1000:
        message_lines.append(f"⚠️ Видимость ограничена: {visibility} м ⚠️")

    # Вывод заката и восхода солнца
    sunrise_formatted = sunrise_timestamp.strftime("%H:%M")
    sunset_formatted = sunset_timestamp.strftime("%H:%M")
    message_lines.append(f"\n🌅 Восход: {sunrise_formatted}")
    message_lines.append(f"🌇 Закат: {sunset_formatted}")

    return '\n'.join(message_lines)


def format_precipitation_forecast(forecast_data):
    """Форматирует информацию об осадках в прогнозе на следующие 24 часа, группируя последовательные периоды осадков"""
    precipitation_intervals = []

    timezone_offset = forecast_data['city']['timezone']  # Смещение в секундах от UTC
    user_timezone = datetime.timezone(datetime.timedelta(seconds=timezone_offset))

    # Получаем текущее время в часовом поясе пользователя
    now = datetime.datetime.now(datetime.timezone.utc).astimezone(user_timezone)
    end_time = now + datetime.timedelta(hours=24)

    current_interval = None  # Текущий интервал осадков

    for item in forecast_data['list']:
        dt_txt = item['dt_txt']
        dt_datetime_utc = datetime.datetime.strptime(dt_txt, '%Y-%m-%d %H:%M:%S').replace(tzinfo=datetime.timezone.utc)
        dt_datetime = dt_datetime_utc.astimezone(user_timezone)

        if now <= dt_datetime <= end_time:
            # Определяем тип осадков
            is_rain = 'rain' in item
            is_snow = 'snow' in item

            precip_type = None
            if is_rain and is_snow:
                precip_type = 'rain and snow'
            elif is_rain:
                precip_type = 'rain'
            elif is_snow:
                precip_type = 'snow'

            if precip_type:
                if current_interval is None:
                    # Начинаем новый интервал осадков
                    current_interval = {
                        'start': dt_datetime,
                        'end': dt_datetime,
                        'type': precip_type
                    }
                elif precip_type == current_interval['type']:
                    # Продолжаем текущий интервал осадков
                    current_interval['end'] = dt_datetime
                else:
                    # Завершаем текущий интервал и начинаем новый
                    precipitation_intervals.append(current_interval)
                    current_interval = {
                        'start': dt_datetime,
                        'end': dt_datetime,
                        'type': precip_type
                    }
            else:
                if current_interval is not None:
                    # Завершаем текущий интервал осадков
                    precipitation_intervals.append(current_interval)
                    current_interval = None

    # Проверяем, остался ли незакрытый интервал осадков
    if current_interval is not None:
        precipitation_intervals.append(current_interval)

    if precipitation_intervals:
        messages = []
        for interval in precipitation_intervals:
            start_dt = interval['start']
            end_dt = interval['end']
            precip_type = interval['type']

            # Определяем, сегодня или завтра
            now_date = now.date()
            start_date = start_dt.date()
            end_date = end_dt.date()

            if start_date == now_date:
                start_date_string = 'Сегодня'
            elif start_date == now_date + datetime.timedelta(days=1):
                start_date_string = 'Завтра'
            else:
                start_date_string = start_dt.strftime('%d.%m')

            if end_date == now_date:
                end_date_string = 'Сегодня'
            elif end_date == now_date + datetime.timedelta(days=1):
                end_date_string = 'Завтра'
            else:
                end_date_string = end_dt.strftime('%d.%m')

            start_time = start_dt.strftime('%H:%M')
            end_time = end_dt.strftime('%H:%M')

            if start_date == end_date:
                # Интервал в пределах одного дня
                message = f"{start_date_string} с {start_time} до {end_time} ожидается {precip_dict[precip_type]}"
            else:
                # Интервал пересекает дни
                message = f"С {start_date_string.lower()} {start_time} до {end_date_string.lower()} {end_time} ожидается {precip_dict[precip_type]}"

            messages.append(message)

            precipitation_message = (
                    "В ближайшие 24 часа ожидаются следующие осадки:\n" +
                    '\n'.join(messages)
            )
            return precipitation_message
    else:
        return 'В ближайшие 24 часа осадков не ожидается! 😉'


def show_weather(message):
    """Функция выводит погоду из JSON на экран пользователя"""

    # Получаем город пользователя
    user_id = message.from_user.id
    conn = sqlite3.connect('../database/users_db.sql')
    cur = conn.cursor()
    cur.execute("SELECT city FROM users WHERE id=?",
                (user_id,))
    result = cur.fetchone()

    if result:

        city = result[0]

        # Получаем текущую погоду
        current_weather_data = get_current_weather(city)
        current_weather_message = format_current_weather(current_weather_data)

        # Получаем прогноз осадков
        forecast_weather_data = get_forecast_weather(city)
        precipitation_message = format_precipitation_forecast(forecast_weather_data)

        # Отправляем информацию о погоде (разными сообщениями в тг)
        bot.send_message(message.chat.id, current_weather_message)
        bot.send_message(message.chat.id, precipitation_message)

    else:
        bot.reply_to(message, f'Произошла непредвиденная ошибка! Пожалуйста, повторите запрос позднее!')

    cur.close()
    conn.close()