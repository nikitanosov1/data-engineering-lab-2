FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        git \
    && rm -rf /var/lib/apt/lists/*

# Установка Python-зависимостей
RUN pip install --no-cache-dir \
    git+https://github.com/m1guelpf/auto-subtitle.git

RUN pip install flask ffmpeg-python

# Копируем приложение
COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]