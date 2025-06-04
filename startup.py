# startup.py
import os
from django.core.management import call_command
from django.db import connection


def run_migrations():
    """Выполняет миграции и создает начальные данные"""
    try:
        print("Database initialization started...")

        # Применяем миграции
        call_command("migrate")

        # Проверяем существование таблицы
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM main_car LIMIT 1")
            print("Database already initialized")
            return
        except Exception:
            pass
        # Создаем начальные данные
        print("Creating initial data...")
        from main.models import Car
        Car.objects.get_or_create(name="KUZANAGI CT-3X")
        Car.objects.get_or_create(name="QUADRA TURBO-R V-TECH")

        print("Database initialization complete!")
    except Exception as e:
        print(f"Initialization failed: {e}")
        # Повторная попытка миграций
        try:
            call_command("migrate")
        except:
            print("Migration retry failed")