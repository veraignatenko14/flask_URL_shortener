import sqlite3
from flask import Flask, render_template, request, redirect, url_for


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # получает строки из БД
    return conn

app = Flask(__name__)
app.config['SECRET_KEY'] = 'try-to-guess'


if __name__ == '__main__':
    app.run()
