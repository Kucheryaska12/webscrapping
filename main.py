import requests
from bs4 import BeautifulSoup
import json


KEYWORDS = ['дизайн', 'фото', 'web', 'python']


responce = requests.get('https://habr.com/ru/articles')
soup = BeautifulSoup(responce.text, features='lxml')
article_list = soup.find_all('article', class_= 'tm-articles-list__item')

parsed_data = []

for article in article_list:
    article_link = 'https://habr.com/ru/articles' + article_list[0].find('a', class_='tm-title__link')['href']
        
    responce1 = requests.get(article_link)
    soup1 = BeautifulSoup(responce1.text, features='lxml')
    article_title = soup1.find('h1').text.strip()
    article_time = soup1.find('time')['datetime']
    article_text = soup1.find('article', class_='tm-article-presenter__content tm-article-presenter__content_narrow').text.strip()
    for word in KEYWORDS:
        if word in article_text:
            parsed_data.append({
                'article_title': article_title,
                'article_taxt': article_text,
                'article_time': article_time
            })

with open('data.json', 'w') as f:
    json.dump(parsed_data, f, ensure_ascii=False, indent=4)