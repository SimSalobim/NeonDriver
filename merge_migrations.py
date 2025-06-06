# merge_migrations.py
import os
import subprocess


def merge_migrations():
    try:
        # Проверяем наличие конфликтующих миграций
        migrations_dir = "main/migrations"
        files = os.listdir(migrations_dir)
        conflicting = [f for f in files if f.startswith("0002") and f.endswith(".py")]

        if len(conflicting) > 1:
            print("Detected conflicting migrations, running merge...")
            # Выполняем команду слияния
            result = subprocess.run(
                ["python", "manage.py", "makemigrations", "--merge", "--noinput"],
                capture_output=True,
                text=True
            )
            print(result.stdout)
            if result.returncode != 0:
                print(f"Merge failed: {result.stderr}")
        else:
            print("No conflicting migrations found")
    except Exception as e:
        print(f"Merge error: {str(e)}")