import re
import sqlite3

def check_company_name(text):
    companies_patterns = {
        'ТМК': r'ТМК|Таганрог|Волжз|Трубн|Челябин|Северск|Первоурал|Металлобаз|Синарск',
        'Евраз': r'Evraz|Евраз',
        'ЗТЗ': r'ЗТЗ|Урал|Загор',
        'Металлоинвест': r'Металлоинвест|Лебедин',
        'ММК': r'ММК|Магнитогор',
        'НЛМК': r'НЛМК|Стойлен|Новолип|ВИЗ-Стал',
        'Северсталь': r'Северсталь|Череповец|Карельск'
    }
    matched_companies = [company for company, pattern in companies_patterns.items() if re.search(pattern, text, re.IGNORECASE)]
    
    if len(matched_companies) == 0:
        return '-'
    elif len(matched_companies) == 1:
        return matched_companies[0]
    else:
        return '?'


def filter_pls():
    # Подключение к базе данных
    connection = sqlite3.connect('news_data.db')
    connection.row_factory = sqlite3.Row  # Позволяет обращаться к столбцам по имени
    cursor = connection.cursor()

    # Получение строк с NULL значением в столбце company
    cursor.execute("SELECT rowid, text FROM news WHERE company IS NULL")
    rows = cursor.fetchall()

    # Применение функции check_company_name к каждой строке и обновление базы данных
    for row in rows:
        text = row['text']  # замените 'text' на имя вашего столбца с текстом
        company_result = check_company_name(text)
        cursor.execute("UPDATE news SET company = ? WHERE rowid = ?", (company_result, row['rowid']))

    # Завершение и сохранение изменений
    connection.commit()
    connection.close()
