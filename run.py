from app import create_app, db

app = create_app()

with app.app_context():
    # Отключаем проверку внешних ключей для MySQL
    db.drop_all()
    db.create_all()
    print("Tables recreated")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)