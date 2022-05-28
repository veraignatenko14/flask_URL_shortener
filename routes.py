from app import app, hashid
from flask import render_template, request, redirect, url_for, flash


@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()  # подключаемся к БД
    if request.method == 'POST':  # если форма отправляется
        url = request.form['url']  # сохраняю урл из формы в переменную
        if not url:  # если поле передали пустым
            flash('The URL is required!')
            return redirect(url_for('index'))
        url_data = conn.execute('INSERT INTO urls (original_url) VALUES (?)', (url,))
        conn.commit()
        conn.close()

        url_id = url_data.lastrowid  # записываю id объекта из БД
        hash_url = hashid.encode(url_id)  # хеширую id урла
        short_url = request.host_url + hash_url
        return render_template('index.html', s_url=short_url)
    return render_template('index.html')
