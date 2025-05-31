from django.db import migrations


def create_initial_cars(apps, schema_editor):
    Car = apps.get_model('main', 'Car')
    Car.objects.create(name="KUZANAGI CT-3X")
    Car.objects.create(name="QUADRA TURBO-R V-TECH")


def reverse_initial_cars(apps, schema_editor):
    Car = apps.get_model('main', 'Car')
    Car.objects.filter(name="KUZANAGI CT-3X").delete()
    Car.objects.filter(name="QUADRA TURBO-R V-TECH").delete()


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_cars, reverse_code=reverse_initial_cars),
    ]