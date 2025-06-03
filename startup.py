# startup.py
import os
import sys
import time
from django.core.management import execute_from_command_line


def run_migrations():
    """Выполняет миграции и создает начальные данные"""
    try:
        print("Starting database initialization...")

        # Применяем миграции
        print("Step 1: Applying migrations...")
        execute_from_command_line(["manage.py", "migrate"])

        # Даем время на применение миграций
        time.sleep(2)

        # Создаем начальные данные
        print("Step 2: Creating initial data...")
        try:
            from main.models import Car
            if not Car.objects.exists():
                Car.objects.get_or_create(name="KUZANAGI CT-3X")
                Car.objects.get_or_create(name="QUADRA TURBO-R V-TECH")
                print("Cars created successfully!")
            else:
                print("Data already exists")
        except Exception as e:
            print(f"Data creation error: {str(e)}")

        print("Database initialization complete!")
        return True
    except Exception as e:
        print(f"Initialization failed: {str(e)}")
        return False