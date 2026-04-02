import pymysql

try:
    # Подключаемся к серверу
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='3620',  # ← Впиши пароль
        charset='utf8mb4'
    )
    
    with conn.cursor() as cursor:
        # Проверяем наличие базы
        cursor.execute("SHOW DATABASES LIKE 'vkr'")
        if cursor.fetchone():
            print("✅ База 'vkr' найдена")
            
            # Проверяем таблицы
            cursor.execute("USE vkr")
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"✅ Найдено таблиц: {len(tables)}")
            for t in tables:
                print(f"   - {t[0]}")
        else:
            print("❌ База 'vkr' не найдена! Выполни импорт SQL файла.")
            
    conn.close()
    
except Exception as e:
    print(f"❌ Ошибка: {e}")