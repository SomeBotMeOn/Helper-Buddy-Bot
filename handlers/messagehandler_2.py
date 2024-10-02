# Обработка других встроенных команд
def weather(message):
    # функция выводит текущую погоду
    res_current_weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_weather}&units=metric')
    bot.reply_to(message, f'Погода в данный момент: {res_current_weather.json()}')



def information(message):
    # Выводит всю информацию о пользователе и чате
    bot.send_message(message.chat.id, message)


def site_with_weather(message):
    # функция отправляет пользователя на сайт с погодой
    webbrowser.open('https://openweathermap.org/weathermap')
