#!/bin/bash
# render-build.sh
pip install -r requirements.txt

set -e

# Применяем миграции
python manage.py migrate

# Собираем статику
python manage.py collectstatic --noinput

# Запускаем сервер
exec gunicorn NeonDrive.wsgi:application