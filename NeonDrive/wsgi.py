# NeonDrive/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NeonDrive.settings')

application = get_wsgi_application()

try:
    from startup import run_migrations
    run_migrations()
except ImportError as e:
    print(f"Startup import error: {e}")
except Exception as e:
    print(f"Initialization error: {e}")