
import os
import sys
from django.core.management import call_command
from django.db import connection


def run_migrations():
    try:
        print("🚀 Starting database initialization...")

        # Проверяем существование таблицы
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM main_car LIMIT 1")
            print("✅ Database already initialized")
            return
        except Exception as e:
            print(f"⚠️ Database not ready: {str(e)}")

        # Применяем миграции
        print("🔄 Applying migrations...")
        call_command("migrate", interactive=False)

        # Создаем начальные данные
        print("✨ Creating initial data...")
        from main.models import Car

        # Создаем автомобили
        Car.objects.get_or_create(name="KUZANAGI CT-3X")
        Car.objects.get_or_create(name="QUADRA TURBO-R V-TECH")

        print("🎉 Database initialization complete!")

    except Exception as e:
        print(f"🔥 Initialization error: {str(e)}")
        import traceback
        traceback.print_exc()

run_migrations()