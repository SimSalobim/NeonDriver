import os
import sys
import time
import django
from django.core.management import call_command
from django.db import connection
from django.db.utils import OperationalError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NeonDrive.settings')

# startup.py
import os
import django
from django.core.management import call_command


def run_migrations():
    try:
        print("=== STARTING INITIALIZATION ===")

        # 1. Применяем миграции
        print("Applying migrations...")
        call_command("migrate")

        # 2. Создаем машины
        print("Creating cars...")
        from main.models import Car
        Car.objects.get_or_create(name="KUZANAGI CT-3X")
        Car.objects.get_or_create(name="QUADRA TURBO-R V-TECH")
        print("Cars created successfully")

        print("=== INITIALIZATION COMPLETE ===")
    except Exception as e:
        print(f"!!! ERROR: {e}")
        import traceback
        traceback.print_exc()

        if wait_for_db():
            run_initialization()
        else:
            sys.exit(1)

def wait_for_db():
    """Ожидание доступности базы данных."""
    max_retries = 10
    retry_delay = 2  # секунды между попытками

    for i in range(max_retries):
        try:
            connection.ensure_connection()
            print("✅ Database connection established")
            return True
        except OperationalError:
            print(f"⚠️ Database not ready, retrying... ({i + 1}/{max_retries})")
            time.sleep(retry_delay)
    print("❌ Max retries reached. Database still not available.")
    return False


def run_initialization():
    """Основная логика инициализации."""
    try:
        print("🚀 Starting database initialization...")

        # Проверка существования таблицы
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables 
                    WHERE table_name = 'main_car'
                )
            """)
            table_exists = cursor.fetchone()[0]

        if table_exists:
            print("✅ Database already initialized")
            return

        # Применение миграций
        print("🔄 Applying migrations...")
        call_command("migrate", interactive=False)

        # Создание начальных данных
        print("✨ Creating initial data...")
        from main.models import Car
        Car.objects.get_or_create(name="KUZANAGI CT-3X")
        Car.objects.get_or_create(name="QUADRA TURBO-R V-TECH")

        print("🎉 Database initialization complete!")
    except Exception as e:
        print(f"🔥 Initialization error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Инициализация Django
    django.setup()

    # Ожидание БД и запуск инициализации
    if wait_for_db():
        run_initialization()
    else:
        sys.exit(1)