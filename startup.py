import os
import sys
from django.core.management import call_command
from django.db import connection, OperationalError


def run_migrations():
    try:
        print("🚀 Starting database initialization...")

        # Проверка подключения к базе данных
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                print("✅ Database connection test successful")
        except OperationalError as e:
            print(f"❌ Database connection failed: {e}")
            raise

        # Применяем миграции
        print("🔄 Applying migrations...")
        call_command("migrate", interactive=False)

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

        # Дополнительная проверка
        print("🔍 Verifying channel layer configuration...")
        from channels.layers import get_channel_layer
        try:
            layer = get_channel_layer()
            print(f"✅ Channel layer configured: {layer}")
        except Exception as e:
            print(f"❌ Channel layer error: {e}")

    except Exception as e:
        print(f"🔥 Initialization failed: {str(e)}")
        import traceback
        traceback.print_exc()