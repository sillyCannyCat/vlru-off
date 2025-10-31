# 😼 VLRU OFF

Это монорепозиторий проекта, включающий фронтенд, бэкенд и библиотеку компонентов.
Каждая часть проекта имеет собственное подробное _README.md_ с инструкциями по установке и запуску, но также настроен docker compose.

## 📂 Структура проекта

```
root/
 ├─ backend/            # Django Ninja API
 │   └─ README.md        # Подробное руководство по backend
 ├─ frontend/           # Vue + Vite + TailwindCSS
 │   └─ README.md        # Подробное руководство по frontend
 └─ silly-canny-lib/    # Vue компонентная библиотека
     └─ README.md        # Подробное руководство по библиотеке компонентов
```

## 🐳 Docker

Для удобства можно поднять одновременно backend и frontend через docker-compose из корня репозитория:

```
docker-compose up --build
```
