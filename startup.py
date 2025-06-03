# startup.py
import os
import sys
from django.db import connection


def run_migrations():
    """Выполняет миграции и создает начальные данные"""
    try:
        # Проверяем, существует ли таблица
        if "main_car" in connection.introspection.table_names():
            return

        print("Applying database migrations...")

        # Применяем миграции
        from django.core.management import execute_from_command_line
        execute_from_command_line(["manage.py", "migrate"])

        # Создаем начальные данные
        print("Creating initial data...")
        from main.models import Car
        Car.objects.get_or_create(name="KUZANAGI CT-3X")
        Car.objects.get_or_create(name="QUADRA TURBO-R V-TECH")

        print("Database initialization complete!")
    except Exception as e:
        print(f"Initialization failed: {str(e)}")