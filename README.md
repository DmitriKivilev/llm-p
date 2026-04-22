# llm-p —  API для работы с LLM через OpenRouter

Учебный проект по разработке ерверного приложения на FastAPI c интеграцией языковой модели, а так же использованием JWT-аунтефикации и SQlite 

# Установка и запуск
pip install uv

# Установка зависимостей
uv sync

# Запуск
uv run uvicorn app.main:app --reload

Swagger: **http://127.0.0.1:8000/docs**

## Демонстрация работы

### Регистрация (student_Kivilev@email.com)
![Регистрация](screenshots/register.png)

### Логин и получение JWT
![Логин](screenshots/login.png)

### Авторизация в Swagger
![Авторизация](screenshots/authorize.png)

### Профиль пользователя
![Профиль](screenshots/me.png)

### Отправка сообщения в LLM
![Чат](screenshots/chat.png)

### История диалога
![История](screenshots/history.png)

### Очистка истории
![Очистка](screenshots/delete.png)

### Пустая история
![Пусто](screenshots/empty.png)

### Проверка работоспособности
![Health](screenshots/health.png)
