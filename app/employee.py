from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from app.decorators import login_required, role_required
from app.models import User, Assignment, Question, Answer, Course, db
from datetime import datetime
import requests

employee_bp = Blueprint('employee', __name__, url_prefix='/employee')

def search_stepik_courses(topic):
    """Ищет курсы на Stepik.org по заданной теме."""
    url = "https://stepik.org/api/courses"
    params = {
        "search": topic,
        "language": "ru",
        "page": 1
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        courses = []
        # Берём первые 3 курса из ответа API
        for course in data.get('courses', [])[:3]:
            courses.append({
                'title': course.get('title', 'Без названия'),
                'description': course.get('summary', '').strip()[:200],
                'url': f"https://stepik.org/course/{course.get('id')}",
                'source': 'Stepik.org',
                'students': course.get('learners_count', 0)
            })
        return courses
    except Exception as e:
        print(f"Ошибка при запросе к Stepik API: {e}")
        return []

@employee_bp.route('/dashboard')
@login_required
@role_required('employee')
def dashboard():
    user_id = session['user_id']
    assignments = Assignment.query.filter_by(employee_id=user_id).all()
    return render_template('employee/dashboard_employee.html',
                           assignments=assignments,
                           username=session['username'])

@employee_bp.route('/test/<int:assignment_id>')
@login_required
@role_required('employee')
def take_test(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    if assignment.employee_id != session['user_id']:
        flash('Доступ запрещён', 'danger')
        return redirect(url_for('employee.dashboard'))
    if assignment.status == 'completed':
        return redirect(url_for('employee.view_result', assignment_id=assignment.id))
    questions = Question.query.filter_by(test_id=assignment.test_id).all()
    return render_template('employee/take_test.html', assignment=assignment, questions=questions)

@employee_bp.route('/test/<int:assignment_id>/submit', methods=['POST'])
@login_required
@role_required('employee')
def submit_test(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    if assignment.employee_id != session['user_id']:
        flash('Доступ запрещён', 'danger')
        return redirect(url_for('employee.dashboard'))
    if assignment.status == 'completed':
        flash('Тест уже пройден', 'warning')
        return redirect(url_for('employee.dashboard'))

    questions = Question.query.filter_by(test_id=assignment.test_id).all()
    total_score = 0
    incorrect_topics = []

    for q in questions:
        answer_text = request.form.get(f'answer_{q.id}')
        is_correct = (answer_text and answer_text.strip() == q.correct_answer.strip())
        points_earned = q.points if is_correct else 0
        total_score += points_earned

        if not is_correct and q.topic:
            incorrect_topics.append(q.topic)

        ans = Answer(
            assignment_id=assignment.id,
            question_id=q.id,
            user_answer=answer_text,
            is_correct=is_correct,
            points_earned=points_earned
        )
        db.session.add(ans)

    assignment.status = 'completed'
    assignment.score = total_score
    assignment.completed_at = datetime.utcnow()
    db.session.commit()

    answers = Answer.query.filter_by(assignment_id=assignment.id).all()

    # Уникальные темы ошибок
    unique_topics = list(set(incorrect_topics))

    # 1. Локальный поиск в БД
    recommended_courses = []
    if unique_topics:
        for topic in unique_topics:
            courses = Course.query.filter(Course.tags.ilike(f'%{topic}%')).all()
            recommended_courses.extend(courses)
        # удаляем дубликаты по id
        seen = set()
        unique_courses = []
        for c in recommended_courses:
            if c.id not in seen:
                seen.add(c.id)
                unique_courses.append(c)
        recommended_courses = unique_courses

    # 2. Поиск внешних ресурсов (Stepik + ссылки)
    external_courses = []
    for topic in unique_topics:
        # Добавляем курсы со Stepik
        stepik_courses = search_stepik_courses(topic)
        external_courses.extend(stepik_courses)
        # Добавляем поисковые ссылки на другие платформы
        external_courses.append({
            'title': f'Поиск курсов по теме "{topic}" на Coursera',
            'url': f'https://www.coursera.org/search?query={topic}',
            'description': f'Курсы на Coursera по теме {topic}',
            'source': 'Coursera'
        })
        external_courses.append({
            'title': f'Курсы по "{topic}" на Udemy',
            'url': f'https://www.udemy.com/courses/search/?q={topic}',
            'description': f'Найдите курсы на Udemy',
            'source': 'Udemy'
        })
        external_courses.append({
            'title': f'Видео по теме "{topic}" на YouTube',
            'url': f'https://www.youtube.com/results?search_query={topic}+курс',
            'description': f'Обучающие видео на YouTube',
            'source': 'YouTube'
        })

    return render_template('employee/result.html',
                           assignment=assignment,
                           answers=answers,
                           recommended_courses=recommended_courses,
                           external_courses=external_courses)

@employee_bp.route('/result/<int:assignment_id>')
@login_required
@role_required('employee')
def view_result(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    if assignment.employee_id != session['user_id']:
        flash('Доступ запрещён', 'danger')
        return redirect(url_for('employee.dashboard'))
    answers = Answer.query.filter_by(assignment_id=assignment.id).all()
    # Здесь можно оставить без рекомендаций, либо при необходимости добавить их повторно
    return render_template('employee/result.html',
                           assignment=assignment,
                           answers=answers,
                           recommended_courses=[])