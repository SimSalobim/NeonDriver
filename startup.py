# startup.py

import os
import sys
from django.core.management import call_command
from django.db import connection, OperationalError


def run_migrations():
    try:
        print("🚀 Starting database initialization...")

        # Проверка подключения к базе данных
        from django.db import connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version()")
                db_version = cursor.fetchone()
                print(f"✅ PostgreSQL version: {db_version[0]}")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            raise

        # Применяем миграции
        print("🔄 Applying migrations...")
        call_command("migrate")

        # Создаем начальные данные
        print("✨ Creating initial data...")
        from main.models import Car

        # Создаем автомобили
        car_names = [
            "KUZANAGI CT-3X",
            "QUADRA TURBO-R V-TECH"
        ]

        for name in car_names:
            car, created = Car.objects.get_or_create(name=name)
            status = "created" if created else "already exists"
            print(f"ℹ️ Car '{name}' {status}")

        car_count = Car.objects.count()
        print(f"🎉 Database initialization complete! Total cars: {car_count}")

    except Exception as e:
        print(f"🔥 Initialization failed: {str(e)}")
        import traceback
        traceback.print_exc()