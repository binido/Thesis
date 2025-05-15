FROM python:3.12-slim

# Установка рабочей директории
WORKDIR /app

# Установка зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Копирование зависимостей
COPY requirements.txt .

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

# Создаем и настраиваем entrypoint.sh
COPY entrypoint.sh /entrypoint.sh
# Преобразуем CRLF в LF и делаем файл исполняемым
RUN dos2unix /entrypoint.sh && chmod +x /entrypoint.sh

# Переменные среды
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Порт для gunicorn
EXPOSE 8000

# Запуск через entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
