# from flask import Flask, render_template, request, redirect, url_for, session, flash
# from functools import wraps

# app = Flask(__name__)
# app.secret_key = 'your-secret-key-here'

# users = {
#     'admin': {
#         'password': 'password',
#         'email': 'admin@example.com',
#         'role': 'hr'
#     },
#     'hr_manager': {
#         'password': 'hrpass',
#         'email': 'hr@example.com',
#         'role': 'hr'
#     }
# }

# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'username' not in session:
#             flash('Пожалуйста, войдите в систему', 'warning')
#             return redirect(url_for('login'))
#         # Проверяем, существует ли пользователь в базе
#         if session['username'] not in users:
#             # Если пользователь удалён или не существует, завершаем сессию
#             session.pop('username', None)
#             flash('Ваша сессия недействительна, войдите заново', 'warning')
#             return redirect(url_for('login'))
#         return f(*args, **kwargs)
#     return decorated_function

# def role_required(role):
#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             if 'username' not in session:
#                 flash('Пожалуйста, войдите в систему', 'warning')
#                 return redirect(url_for('login'))
#             user = users.get(session['username'])
#             if not user or user.get('role') != role:
#                 flash('Доступ запрещён', 'danger')
#                 return redirect(url_for('dashboard'))
#             return f(*args, **kwargs)
#         return decorated_function
#     return decorator

# @app.route('/')
# @login_required
# def index():
#     user = users.get(session['username'])
#     if user['role'] == 'hr':
#         return redirect(url_for('dashboard_hr'))
#     else:
#         return redirect(url_for('dashboard_employee'))

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         user = users.get(username)
#         if user and user['password'] == password:
#             session['username'] = username
#             flash('Вы успешно вошли', 'success')
#             return redirect(url_for('index'))
#         else:
#             flash('Неверный логин или пароль', 'danger')
#     return render_template('login.html')

# @app.route('/register', methods=['POST'])
# def register():
#     username = request.form.get('username')
#     email = request.form.get('email')
#     password = request.form.get('password')
#     confirm = request.form.get('confirm_password')

#     if not username or not email or not password or not confirm:
#         flash('Все поля обязательны для заполнения', 'danger')
#         return redirect(url_for('login'))

#     if username in users:
#         flash('Пользователь с таким логином уже существует', 'danger')
#         return redirect(url_for('login'))

#     if password != confirm:
#         flash('Пароли не совпадают', 'danger')
#         return redirect(url_for('login'))

#     if '@' not in email:
#         flash('Введите корректный email', 'danger')
#         return redirect(url_for('login'))

#     users[username] = {
#         'password': password,
#         'email': email,
#         'role': 'hr'
#     }
#     flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
#     return redirect(url_for('login'))

# @app.route('/dashboard/hr')
# @login_required
# @role_required('hr')
# def dashboard_hr():
#     hr_name = session['username']
#     employees = []
#     for username, data in users.items():
#         if data.get('role') == 'employee' and data.get('created_by') == hr_name:
#             employees.append({'username': username, 'email': data['email']})
#     return render_template('dashboard_hr.html', employees=employees)

# @app.route('/dashboard/employee')
# @login_required
# @role_required('employee')
# def dashboard_employee():
#     return render_template('dashboard_employee.html', username=session['username'])

# @app.route('/create_employee', methods=['POST'])
# @login_required
# @role_required('hr')
# def create_employee():
#     hr_name = session['username']
#     username = request.form.get('username')
#     email = request.form.get('email')
#     password = request.form.get('password')
#     confirm = request.form.get('confirm_password')

#     if not username or not email or not password or not confirm:
#         flash('Все поля обязательны для заполнения', 'danger')
#         return redirect(url_for('dashboard_hr'))

#     if username in users:
#         flash('Пользователь с таким логином уже существует', 'danger')
#         return redirect(url_for('dashboard_hr'))

#     if password != confirm:
#         flash('Пароли не совпадают', 'danger')
#         return redirect(url_for('dashboard_hr'))

#     if '@' not in email:
#         flash('Введите корректный email', 'danger')
#         return redirect(url_for('dashboard_hr'))

#     users[username] = {
#         'password': password,
#         'email': email,
#         'role': 'employee',
#         'created_by': hr_name
#     }
#     flash(f'Сотрудник {username} успешно создан', 'success')
#     return redirect(url_for('dashboard_hr'))

# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     flash('Вы вышли из системы', 'info')
#     return redirect(url_for('login'))

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=8080)