# main/apps.py
from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        # УДАЛИТЬ ВЕСЬ КОД ИЗ ЭТОГО МЕТОДА
        # Оставьте метод пустым или полностью удалите его
        pass