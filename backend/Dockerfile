# 1. Use an official lightweight Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# --- Best Practice: Create a non-root user for security ---
# Создаем группу и пользователя 'app' для запуска приложения
RUN addgroup --system app && adduser --system --ingroup app app
# Устанавливаем домашнюю директорию для пользователя 'app', чтобы утилиты, такие как uv,
# могли корректно создавать свои кэши и временные файлы.
ENV HOME=/app

# 2. Set up the working directory
WORKDIR /app
# Рабочая директория создается от имени root, поэтому меняем владельца на 'app'.
# Это позволит нашему пользователю создавать файлы, например .venv, в рабочей директории.
RUN chown app:app /app

# 3. Install uv, our package manager
RUN pip install uv

# 4. Copy only the dependency definitions to leverage Docker's cache
# Копируем файлы от имени нового пользователя, чтобы права были корректными
COPY --chown=app:app backend/pyproject.toml backend/uv.lock ./

# 5. Install project dependencies
# Переключаемся на пользователя 'app' ПЕРЕД установкой зависимостей и запуском
USER app
RUN uv sync --no-cache

# 6. Copy the application's source code
# Копируем только папку с исходным кодом, а не всё подряд
COPY --chown=app:app backend/src ./src

# 7. Define the command to run the application
EXPOSE 8000
# Используем uv run для запуска в виртуальном окружении.
# Явно указываем host 0.0.0.0, чтобы сервис был доступен извне контейнера.
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]