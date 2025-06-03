# main/migrations/0002_create_initial_data.py
from django.db import migrations


def create_cars(apps, schema_editor):
    Car = apps.get_model('main', 'Car')
    Car.objects.get_or_create(name="KUZANAGI CT-3X")
    Car.objects.get_or_create(name="QUADRA TURBO-R V-TECH")


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_cars),
    ]