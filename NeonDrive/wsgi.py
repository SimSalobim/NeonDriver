# NeonDrive/wsgi.py
import os
import sys
from django.core.wsgi import get_wsgi_application

# Добавляем путь к проекту
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_path not in sys.path:
    sys.path.append(project_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NeonDrive.settings')

# Инициализация базы данных
try:
    from startup import run_migrations
    run_migrations()
except ImportError as e:
    print(f"Startup import error: {e}")

application = get_wsgi_application()