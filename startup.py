# startup.py
import os
from django.core.management import call_command
from django.db import connection


def run_migrations():
    try:
        print("Checking database status...")

        # Проверяем существование таблицы через raw SQL
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM main_car LIMIT 1")
            print("Database already initialized")
            return
        except Exception:
            pass

        # Применяем миграции
        print("Applying migrations...")
        call_command("migrate")

        # Создаем начальные данные
        print("Creating initial data...")
        from main.models import Car
        Car.objects.get_or_create(name="KUZANAGI CT-3X")
        Car.objects.get_or_create(name="QUADRA TURBO-R V-TECH")

        print("Database initialization complete!")
    except Exception as e:
        print(f"Initialization failed: {e}")
        # Повторная попытка
        try:
            call_command("migrate")
        except:
            print("Retry failed")