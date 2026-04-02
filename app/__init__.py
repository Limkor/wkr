from flask import Flask, redirect, url_for, session
from config import Config
from app.decorators import login_required
from app.models import db, User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.auth import auth_bp
    from app.hr import hr_bp
    from app.employee import employee_bp


    app.register_blueprint(auth_bp)
    app.register_blueprint(hr_bp)
    app.register_blueprint(employee_bp)


    @app.route('/')
    @login_required
    def index():
        user = User.query.get(session['user_id'])
        if user is None:
            session.pop('user_id', None)
            return redirect(url_for('auth.login'))
        if user.role == 'hr':
            return redirect(url_for('hr.dashboard'))
        elif user.role == 'employee':
            return redirect(url_for('employee.dashboard'))
        else:
            # Неизвестная роль
            return redirect(url_for('auth.login'))
    return app