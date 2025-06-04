# main/apps.py
from multiprocessing import connection

from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        # Импортируем здесь, чтобы избежать циклических импортов
        from .models import Car
        from django.db.models.signals import post_migrate

            # Проверяем, что таблица существует
        Car.objects.get_or_create(name="KUZANAGI CT-3X")
        Car.objects.get_or_create(name="QUADRA TURBO-R V-TECH")
