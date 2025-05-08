import requests
from bs4 import BeautifulSoup
import json
from fake_headers import Headers


KEYWORDS = ['дизайн', 'фото', 'web', 'python']


responce = requests.get('https://habr.com/ru/articles', headers=Headers(browser='chrome', os='win').generate())
soup = BeautifulSoup(responce.text, features='lxml')
article_list = soup.find_all('article', class_= 'tm-articles-list__item')

parsed_data = []
for article in article_list:
    article_link = 'https://habr.com' + article.find('a', class_='tm-title__link')['href']
    responce1 = requests.get(article_link, headers=Headers(browser='chrome', os='win').generate())
    soup1 = BeautifulSoup(responce1.text, features='lxml')
    article_title = soup1.find('h1').text.strip()
    article_time = soup1.find('time')['datetime']
    article_text = soup1.find('article', class_='tm-article-presenter__content tm-article-presenter__content_narrow').text.strip()
    for word in KEYWORDS:
        if word in article_text or article_title:
            parsed_data.append({
                'article_time': article_time[:10],
                'article_title': article_title,
                'article_link': article_link
            })
        break
    
with open('data.json', 'w', encoding="utf-8") as f:
    json.dump(parsed_data, f, ensure_ascii=False, indent=4)

  