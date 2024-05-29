import sqlite3

# Подключение к базе данных
connection = sqlite3.connect('news_data.db')
cursor = connection.cursor()

# Заполнение всех значений в столбце added_to_xls значением FALSE
cursor.execute('UPDATE news SET added_to_xls = FALSE')

# Завершение и сохранение изменений
connection.commit()
connection.close()
