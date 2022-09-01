import sys
import sqlite3

dbPath = 'cartridge.db'
table1 = 'Картриджи'
table2 = 'Операции'
sort = 1

# Переименование столбца с инвентарными номерами картриджей
db = sqlite3.connect(dbPath)
c = db.cursor()

# запрос данных из базы
c.execute(f'SELECT * FROM {table1} ORDER BY {sort};')
items = c.fetchall()

c.executemany(f'UPDATE {table2} SET Заправка = ?;', '1')
db.commit()

# закрытие подключения
db.close()