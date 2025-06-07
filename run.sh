#!/bin/bash

# Запуск инициализации БД
echo "🔄 Запуск инициализации базы данных..."
python startup.py
EXIT_CODE=$?

# Проверка статуса инициализации
if [ $EXIT_CODE -ne 0 ]; then
    echo "❌ Ошибка инициализации БД. Код выхода: $EXIT_CODE"
    exit $EXIT_CODE
fi

# Запуск сервера
echo "🚀 Запуск сервера Daphne на порту $PORT..."
exec daphne NeonDrive.asgi:application --port $PORT --bind 0.0.0.0