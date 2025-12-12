FROM python:3.11-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Чтобы Python нормально логировал
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение
COPY app ./app

# Копируем Alembic
COPY alembic.ini ./alembic.ini
COPY alembic ./alembic

# Открываем порт
EXPOSE 8000

# Запуск FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
