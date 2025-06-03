#!/bin/bash
# render-build.sh
set -e

# Применяем миграции
python manage.py migrate

# Собираем статику
pip install -r requirements.txt && python manage.py collectstatic --noinput

# Запускаем сервер
exec gunicorn NeonDrive.wsgi:application