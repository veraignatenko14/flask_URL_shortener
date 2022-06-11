from flask import Flask
from hashids import Hashids
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)  # подключаю конфигурационный файл к сайту
db = SQLAlchemy(app)  # "дружу" базу данных с сайтом
migrate = Migrate(app, db)  # учу БД регистрировать изменения в своей структуре
login = LoginManager(app)  # подключаю логины пользователей
hashid = Hashids(min_length=4, salt=app.config['SECRET_KEY'])

from routes import *

if __name__ == '__main__':
    app.run(address='0.0.0.0')
