FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /bot

# Зависимости ставим отдельным слоем, чтобы они кэшировались между сборками
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app ./app

# Бот работает не от root
RUN useradd --create-home --uid 1000 bot
USER bot

# Запуск из корня проекта: код читает app/music/genres.json по относительному пути
CMD ["python", "app/main.py"]
