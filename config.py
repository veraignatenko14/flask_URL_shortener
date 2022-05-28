import os

basedir = os.path.abspath(os.path.dirname(__file__))
"""
abspath - абсолютный путь 
path.dirname(__file__) - получить путь к 
исполняемому (этому) 
"""


class Config:
    SECRET_KEY = 'try-to-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')  # sqlite:////Users/demidraksin/PycharmProjects/flask_URL_shortener/app.db
    # сайт сам найдет путь к базе данных, сложив sqlite с путем к файлу БД
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # отменить отслеживание изменений в структуре БД
