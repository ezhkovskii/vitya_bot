# Используем официальный Python образ
FROM python:3.13-slim-bookworm

RUN pip install --no-cache-dir uv

RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY src/ ./src/

CMD ["uv", "run", "src/main.py"]