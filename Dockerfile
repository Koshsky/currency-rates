FROM python:3.11-slim

# Установка необходимых пакетов для GUI и сети
RUN apt-get update && apt-get install -y \
    python3-tk \
    x11-apps \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install poetry

# Создание рабочей директории
WORKDIR /app

# Копирование файлов проекта
COPY pyproject.toml poetry.lock* ./
COPY main.py ./

# Установка зависимостей
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Установка переменных окружения для GUI
ENV DISPLAY=:0
ENV PYTHONUNBUFFERED=1

# Команда запуска
CMD ["poetry", "run", "python3", "main.py"]
