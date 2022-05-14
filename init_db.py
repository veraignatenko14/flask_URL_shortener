import sqlite3

connection = sqlite3.connect('database.db')
# подключение (создание) БД

with open('schema.sql') as file:
    connection.executescript(file.read())

connection.commit()  # сохранить изменения в БД
connection.close()  # закрыть соединение с БД
