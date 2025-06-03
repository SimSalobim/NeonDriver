"""
WSGI config for NeonDrive project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

# NeonDrive/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NeonDrive.settings')

# Инициализация базы данных
if os.environ.get('RUN_INIT') == 'true':
    from startup import initialize_database
    initialize_database()

application = get_wsgi_application()