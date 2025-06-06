
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
        call_command("migrate")

        # Создаем начальные данные
        print("✨ Creating initial data...")
        from main.models import Car

        # Создаем первый автомобиль
        car1, created1 = Car.objects.get_or_create(name="KUZANAGI CT-3X")
        if created1:
            print(f"✅ Car 1 created successfully: {car1.name}")
        else:
            print(f"ℹ️ Car 1 already exists: {car1.name}")

        # Создаем второй автомобиль
        car2, created2 = Car.objects.get_or_create(name="QUADRA TURBO-R V-TECH")
        if created2:
            print(f"✅ Car 2 created successfully: {car2.name}")
        else:
            print(f"ℹ️ Car 2 already exists: {car2.name}")

        # Проверяем итог
        car_count = Car.objects.count()
        print(f"🎉 Database initialization complete! Total cars: {car_count}")

    except Exception as e:
        print(f"🔥 Initialization failed: {str(e)}")
        import traceback
        traceback.print_exc()