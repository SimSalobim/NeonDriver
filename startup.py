# startup.py
import os
import sys
import logging
from django.core.management import execute_from_command_line
from django.db import connection


def initialize_database():
    """Выполняет миграции и создает начальные данные"""
    try:
        # Применяем миграции
        print("Applying database migrations...")
        execute_from_command_line(["manage.py", "migrate"])

        # Проверяем, есть ли уже данные в базе
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM main_car")
            count = cursor.fetchone()[0]

            if count == 0:
                print("Creating initial data...")
                create_initial_data()

        print("Database initialization complete!")
    except Exception as e:
        logging.exception("Database initialization failed")


def create_initial_data():
    """Создает начальные данные"""
    from main.models import Car

    cars = [
        {"name": "KUZANAGI CT-3X"},
        {"name": "QUADRA TURBO-R V-TECH"},
    ]

    for car_data in cars:
        Car.objects.get_or_create(**car_data)