from flask import Blueprint, render_template, request, redirect, url_for, flash, session
# from app.models import get_user, user_exists, create_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Вы успешно вошли', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверный логин или пароль', 'danger')
    return render_template('login.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm = request.form.get('confirm_password')

    if not all([username, email, password, confirm]):
        flash('Все поля обязательны для заполнения', 'danger')
        return redirect(url_for('auth.login'))
    
    if User.query.filter_by(username=username).first():
        flash('Пользователь с таким логином уже существует', 'danger')
        return redirect(url_for('auth.login'))
    
    if password != confirm:
        flash('Пароли не совпадают', 'danger')
        return redirect(url_for('auth.login'))
    
    if '@' not in email:
        flash('Введите корректный email', 'danger')
        return redirect(url_for('auth.login'))
    
    user = User(username=username, email=email, password=generate_password_hash(password), role='hr')
    db.session.add(user)
    db.session.commit()
    flash('Регистрация успешна', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('auth.login'))