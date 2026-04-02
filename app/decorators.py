from functools import wraps
from flask import session, flash, redirect, url_for
from app.models import User, db


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите в систему', 'warning')
            return redirect(url_for('auth.login'))
        # if not get_user(session['username']):
        #     session.pop('username', None)
        #     flash('Ваша сессия недействительна, войдите заново', 'warning')
        #     return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'user_id' not in session:
                flash('Пожалуйста, войдите в систему', 'warning')
                return redirect(url_for('auth.login'))
            user = User.query.get(session['user_id'])
            if not user or user.role != role:
                flash('Доступ запрещён', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated
    return decorator