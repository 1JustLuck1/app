# ===== STAGE 1: Builder =====
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml ./
COPY uv.lock* ./

# 🔥 Установка зависимостей прямо в систему builder
RUN uv pip install --system --no-cache -r pyproject.toml

# ===== STAGE 2: Runtime =====
FROM python:3.12-slim AS runtime

# Создаём непривилегированного пользователя
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# 🔥 Копируем установленные пакеты из builder
COPY --from=builder --chown=appuser:appuser /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder --chown=appuser:appuser /usr/local/bin/uvicorn /usr/local/bin/uvicorn

# Копируем исходный код
COPY --chown=appuser:appuser . .

# Переключаемся на пользователя
USER appuser

# Переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# 🔥 Запуск приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]