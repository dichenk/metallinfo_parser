import requests
from bs4 import BeautifulSoup
import time
import datetime
import random
import sqlite3


BASE_URL = "https://www.metalinfo.ru/ru/news/rferrous.html"
BASE_LINK_URL = "https://www.metalinfo.ru"
START_PAGE = 1
END_PAGE = 5


def get_news_links(page):
    url = f"{BASE_URL}?pn={page}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    news_list = soup.find('div', class_='news-list')
    news_blocks = news_list.find_all('div', class_='news-block clearfix')

    links = []
    for block in news_blocks:
        a_tag = block.find('a', href=True)
        if a_tag:
            links.append(BASE_LINK_URL + a_tag['href'])
    return links


def get_news_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    title_element = soup.find('h1', class_='news-title')
    if title_element:
        title = title_element.get_text(strip=True)
    else:
        title = "Заголовок не найден"

    news_body = soup.find('div', class_='news-body')
    if news_body:
        body_section = news_body.find('section', itemprop='text')
        if body_section:
            paragraphs = body_section.find_all('p')
            text = "\n".join(p.get_text(strip=True) for p in paragraphs)
        else:
            text = "Текст не найден"
    else:
        text = "Блок с новостью не найден"

    topics = ";".join([topic.get_text(strip=True) for topic in soup.find_all('a', class_='news-topics')])

    news_date = soup.find('span', class_='news-date')
    if news_date:
        date_published = news_date.find('meta', itemprop='datePublished')['content']
        time_published = news_date.get_text(strip=True).split('|')[1].strip()
    else:
        date_published = "Дата не найдена"
        time_published = "Время не найдено"

    return title, text, topics, date_published, time_published


def parse_pls():
    conn = sqlite3.connect('news_data.db')
    cursor = conn.cursor()

    # Создание таблицы, если она не существует
    cursor.execute('''CREATE TABLE IF NOT EXISTS news (
                        link TEXT PRIMARY KEY,
                        title TEXT,
                        text TEXT,
                        topics TEXT,
                        date_published1 TEXT,
                        time_published2 TEXT,
                        created_at TEXT TEXT DEFAULT CURRENT_TIMESTAMP
                    )''')

    # Получение последней записи из таблицы
    cursor.execute("SELECT link FROM news")
    result = cursor.fetchall()
    link_list = [row[0] for row in result]

    # Код для сбора данных
    for page in range(START_PAGE, END_PAGE + 1):
        brk = False
        news_data = []
        print(f"Парсинг страницы {page}")
        links = get_news_links(page)

        for link in links:
            if link in link_list:
                print(f"Новость {link} уже добавлена")
                time.sleep(random.uniform(1, 10))
                brk = True
                break  # Достигнута последняя запись
            print(f"Парсинг новости: {link}")
            try:
                title, text, topics, date_published1, time_published2 = get_news_details(link)
                news_data.append([link, title, text, topics, date_published1, time_published2])
                print(f"Новость {link}\n{title}\n{text}\n{topics}\n{time_published2}\nуспешно добавлена")
                time.sleep(random.uniform(1, 10))
            except requests.RequestException as e:
                print(f"Произошла ошибка при запросе: {e}")
                time.sleep(random.uniform(1, 10))
                break
        if brk:
            break

        # Сохранение данных в базу данных SQLite
        cursor.executemany("INSERT OR IGNORE INTO news (link, title, text, topics, date_published1, time_published2, created_at) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)", news_data)
        conn.commit()

    # Закрытие соединения с базой данных
    conn.close()