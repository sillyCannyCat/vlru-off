# 🐍😼 backend

REST API сервер на Django с использованием Django Ninja для быстрого создания API с автогенерацией документации.

## 📄 Автодокументация эндпойнтов

```
http://127.0.0.1:8000/api/docs - для dev сервера
```

## 🛠 Установка и запуск

Рекомендуется использовать виртуальное окружение:

```
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

Применяем миграции:

```
python manage.py migrate
```

Запуск dev сервера:

```
python manage.py runserver
```
