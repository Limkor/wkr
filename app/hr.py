from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.decorators import login_required, role_required
from app.models import User, Test, Question, Assignment, Answer, db
from werkzeug.security import generate_password_hash

hr_bp = Blueprint('hr', __name__, url_prefix='/hr')

@hr_bp.route('/dashboard')
@login_required
@role_required('hr')
def dashboard():
    hr_id = session['user_id']
    tests = Test.query.all()  # все тесты
    employees = User.query.filter_by(role='employee', created_by=hr_id).all()
    assignments = Assignment.query.join(Test).filter(Test.created_by == hr_id).all()
    return render_template('hr/dashboard_hr.html', tests=tests, employees=employees, assignments=assignments)

@hr_bp.route('/test/create', methods=['GET', 'POST'])
@login_required
@role_required('hr')
def create_test():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        test = Test(title=title, description=description, created_by=session['user_id'])
        db.session.add(test)
        db.session.commit()
        i = 1
        while f'question_{i}' in request.form:
            q_text = request.form.get(f'question_{i}')
            correct = request.form.get(f'correct_{i}')
            points = request.form.get(f'points_{i}', 1)
            topic = request.form.get(f'topic_{i}')          # <-- добавить
            if q_text and correct:
                question = Question(
                    test_id=test.id,
                    question=q_text,
                    correct_answer=correct,
                    points=int(points),
                    topic=topic                             # <-- добавить
                )
                db.session.add(question)
            i += 1
        db.session.commit()
        flash('Тест создан', 'success')
        return redirect(url_for('hr.dashboard'))
    return render_template('hr/create_tests.html')

@hr_bp.route('/test/<int:test_id>/assign', methods=['POST'])
@login_required
@role_required('hr')
def assign_test(test_id):
    test = Test.query.get_or_404(test_id)
    employee_ids = request.form.getlist('employee_ids')
    for emp_id in employee_ids:
        existing = Assignment.query.filter_by(test_id=test_id, employee_id=emp_id).first()
        if not existing:
            assignment = Assignment(test_id=test_id, employee_id=emp_id, status='assigned')
            db.session.add(assignment)
    db.session.commit()
    flash('Назначения выполнены', 'success')
    return redirect(url_for('hr.dashboard'))

@hr_bp.route('/assignment/<int:assignment_id>')
@login_required
@role_required('hr')
def view_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    answers = Answer.query.filter_by(assignment_id=assignment.id).all()
    return render_template('hr/assignment_detail.html', assignment=assignment, answers=answers)

@hr_bp.route('/create_employee', methods=['POST'])
@login_required
@role_required('hr')
def create_employee():
    hr_id = session['user_id']
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm = request.form.get('confirm_password')

    if not all([username, email, password, confirm]):
        flash('Все поля обязательны для заполнения', 'danger')
        return redirect(url_for('hr.dashboard'))

    if User.query.filter_by(username=username).first():
        flash('Пользователь с таким логином уже существует', 'danger')
        return redirect(url_for('hr.dashboard'))

    if password != confirm:
        flash('Пароли не совпадают', 'danger')
        return redirect(url_for('hr.dashboard'))

    if '@' not in email:
        flash('Введите корректный email', 'danger')
        return redirect(url_for('hr.dashboard'))

    user = User(username=username, email=email, password=generate_password_hash(password), role='employee', created_by=hr_id)
    db.session.add(user)
    db.session.commit()
    flash(f'Сотрудник {username} успешно создан', 'success')
    return redirect(url_for('hr.dashboard'))