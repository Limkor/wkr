# wkr

> Веб-приложение для управления сотрудниками и тестирования на базе Flask

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-black.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📖 Описание

**wkr** — это веб-приложение для управления персоналом и проведения тестирования сотрудников. Система поддерживает разделение ролей (HR-менеджер / Сотрудник), создание тестов, назначение заданий и отслеживание результатов.

## ✨ Основные возможности

- 🔐 **Аутентификация**: регистрация, вход, выход из системы
- 👥 **Ролевая модель**:
  - `hr` — создание сотрудников, тестов, назначение заданий
  - `employee` — прохождение тестов, просмотр результатов
- 📝 **Управление тестами**:
  - Создание тестов с вопросами и правильными ответами
  - Привязка вопросов к темам, настройка баллов
- 📊 **Назначение и отслеживание**:
  - Назначение тестов сотрудникам
  - Статусы: `assigned`, `in_progress`, `completed`
  - Подсчёт баллов и фиксация времени завершения
- 🎓 **Курсы**: управление обучающими материалами (название, описание, уровень, теги, ссылка)

## 🗂️ Структура проекта
├── app/ # Основной пакет приложения
│ ├── init.py # Фабрика приложения, регистрация blueprint'ов
│ ├── auth.py # Маршруты аутентификации
│ ├── hr.py # Маршруты для HR-менеджеров
│ ├── employee.py # Маршруты для сотрудников
│ ├── decorators.py # Декораторы @login_required, @role_required
│ ├── models.py # SQLAlchemy модели (User, Test, Question, Assignment, Answer, Course)
│ ├── static/ # Статические файлы (CSS, JS, изображения)
│ └── templates/ # Jinja2 HTML-шаблоны
├── config.py # Конфигурация приложения (БД, SECRET_KEY)
├── run.py # Точка входа: инициализация БД и запуск сервера
├── check_db.py # Утилита для проверки подключения к БД

## 🛠️ Технологии

- **Backend**: Python 3.8+, Flask, Flask-SQLAlchemy
- **База данных**: MySQL (через PyMySQL)
- **Frontend**: HTML5, CSS3, JavaScript
- **Шаблоны**: Jinja2

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/Limkor/wkr.git
cd wkr
```
### 2. Создание виртуального окружения
```bash
python -m venv venv
# Для Windows:
venv\Scripts\activate
# Для Linux/Mac:
source venv/bin/activate
```

### 3. Установка зависимостей
```
pip install flask flask-sqlalchemy pymysql python-dotenv
# Или, если есть requirements.txt:
pip install -r requirements.txt
```

### 4. Настройка конфигурации
```
SECRET_KEY = 'your-secure-secret-key'  # Замените на надёжный ключ

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost:3306/vkr?charset=utf8mb4'
# Рекомендуется использовать переменные окружения:
# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
```
