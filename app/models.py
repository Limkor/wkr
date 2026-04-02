from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Связи: тесты, созданные пользователем
    created_tests = db.relationship(
        'Test',
        backref='creator',
        lazy=True,
        foreign_keys='Test.created_by'   # указываем явно, какой внешний ключ
    )
    # Назначения как сотрудник
    assignments = db.relationship(
        'Assignment',
        backref='employee',
        lazy=True,
        foreign_keys='Assignment.employee_id'
    )
class Test(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    questions = db.relationship('Question', backref='test', lazy=True, cascade='all, delete-orphan')
    assignments = db.relationship('Assignment', backref='test', lazy=True)

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.String(200), nullable=False)  # для простоты – текстовый ответ
    points = db.Column(db.Integer, default=1)
    topic = db.Column(db.String(100))
    answers = db.relationship('Answer', backref='question', lazy=True, cascade='all, delete-orphan')

class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='assigned')  # assigned, in_progress, completed
    score = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime)
    # Связь с ответами
    answers = db.relationship('Answer', backref='assignment', lazy=True, cascade='all, delete-orphan')

class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    user_answer = db.Column(db.String(200))
    is_correct = db.Column(db.Boolean, default=False)
    points_earned = db.Column(db.Integer, default=0)

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    duration = db.Column(db.String(50))
    level = db.Column(db.String(20))
    tags = db.Column(db.String(200))
    url = db.Column(db.String(500))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    creator = db.relationship('User', backref='created_courses')
# users = {
#     'admin': {
#         'password': 'password',
#         'email': 'admin@example.com',
#         'role': 'hr'
#     },
#     'hr':{
#         'password': 'hr',
#         'email': 'hr@example.com',
#         'role': 'hr'
#     }
# }

# def get_user(username):
#     return users.get(username)

# def create_user(username, email, password, role, created_by=None):
#     users[username] = {
#         'password': password,
#         'email': email,
#         'role': role,
#         'created_by': created_by
#     }

# def user_exists(username):
#     return username in users

# def get_employees_by_hr(hr_name):
#     return [
#         {'username': u, 'email': data['email']}
#         for u, data in users.items()
#         if data.get('role') == 'employee' and data.get('created_by') == hr_name
#     ]