import hashlib
from app import app, hashid, login, db
from flask import render_template, request, redirect, url_for, flash
from models import User, Url


@login.user_loader
def load_user(id):
    return User.query.get(id)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # если форма отправляется
        url = request.form['url']  # сохраняю урл из формы в переменную
        if not url:  # если поле передали пустым
            flash('The URL is required!')
            return redirect(url_for('index'))
        hash_link = hashlib.sha256(bytes(url, 'ascii'))
        new_url = Url(
            original_url=url,
            short_url=hash_link.hexdigest(),
            user_id=1
        )
        db.session.add(new_url)
        db.session.commit()
        return render_template('index.html')
    return render_template('index.html')
