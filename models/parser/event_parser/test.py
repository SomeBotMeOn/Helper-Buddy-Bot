import requests
from bs4 import BeautifulSoup

url = 'https://afisha.yandex.ru/moscow/selections/nearest-events'
headers = {'accept': '*/*',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
}

req = requests.get(url, headers=headers)
src = req.text
# print(src)
soup = BeautifulSoup(src, "lxml")

from colorama import Style

events = soup.find_all("div", class_="event events-list__item yandex-sans")
events_url = soup.find_all("div", class_="Badges-njdnt8-7 eSHAvL")#.find('a')
url = 'https://afisha.yandex.ru'

events_name_list = []
for item in events:
    name = item.find("div", class_="Root-fq4hbj-4 iFrhLC").find('h2')
    events_name_list.append(name.text)

events_url_list = []
for item in events_url:
    events_url_list.append(url + item.find('a').get('href'))

print(Style.BRIGHT + 'События в ближайшие дни' + Style.BRIGHT + '\n')
for i in range(len(events_name_list)):
    print(events_name_list[i])
    print(events_url_list[i], '\n')