from app import app, hashid, login, db
from flask import render_template, request, redirect, url_for, flash
from models import User, Url
from flask_login import current_user, login_user, logout_user, login_required
from forms import LoginForm, RegistrationForm, UpdateUrlForm
from wtforms.validators import ValidationError


@login.user_loader
def load_user(id):
    return User.query.get(id)


@app.route('/', methods=['GET', 'POST'])
def index():
    urls = Url.query.all()
    if request.method == 'POST':  # если форма отправляется
        url = request.form['url']  # сохраняю урл из формы в переменную
        url_id = urls[-1].id + 1  # id самой последней ссылки в БД + 1
        if not url:  # если поле передали пустым
            flash('Нужна ссылка!', 'warning')
            return redirect(url_for('index'))
        hash_link = hashid.encode(url_id)
        new_url = Url(
            original_url=url,
            short_url=hash_link,
            user_id=current_user.id  # привязываем сокращенную ссылку к пользователю
        )
        db.session.add(new_url)
        db.session.commit()
        flash(f'Ваш URL успешно сокращен: {request.host_url}{hash_link}', 'success')
        flash(f'URL successfully shortened: {request.host_url}{hash_link}', 'success')
        return render_template('index.html')
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():  # если форма отправляется
        user = User.query.filter_by(username=form.username.data).first()  # пытаюсь найти пользователя в БД по логину
        if user is None or not user.check_password(form.password.data):
            # если пользователь не найден в БД или пароль не совпал
            return redirect(url_for('login'))  # вернуть пользователя на страницу входа
        login_user(user, remember=form.remember_me.data)
        flash('Logged in!', 'info')
        return redirect(url_for('index'))
    return render_template('login.html', title='Login page', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # если пользователь вошел
        return redirect(url_for('index'))  # перенаправим на главную
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            form.check_username(form.username)
            form.check_email(form.email)
            user = User(
                username=form.username.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            db.session.add(user)  # добавить пользователя в БД
            db.session.commit()  # сохранить пользователя в БД
            return redirect(url_for('login'))  # перенаправить на страницу входа
        except ValidationError:
            flash('Username or email already exists!', 'danger')
            return redirect(url_for('register'))
    return render_template('register.html', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    urls = Url.query.filter_by(user_id=user.id)
    return render_template('user.html', user=user, urls=urls)


@app.route('/<short_url>')
def redirect_to(short_url):
    url = Url.query.filter_by(short_url=short_url).first_or_404()
    url.clicks += 1
    db.session.commit()  # применить изменения в базе
    return redirect(url.original_url)


@app.route('/update-url/<short_url>', methods=['GET', 'POST'])
def update_url(short_url):
    url = Url.query.filter_by(short_url=short_url).first_or_404()
    form = UpdateUrlForm()
    if form.validate_on_submit():
        url.short_url = form.url.data
        try:
            db.session.commit()
        except:
            return 'There was a problem updating data'
        flash(f'URL successfully changed: {request.host_url}{url.short_url}', 'success')
        return redirect(url_for('index')) # вписываю в поле URL текущее значение сокращенной ссылки
    return render_template('update_url.html', form=form)
