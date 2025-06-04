#!/bin/bash
# render-build.sh
pip install -r requirements.txt

python manage.py collectstatic --noinput

set -e

# Применяем миграции
python manage.py migrate


# Запускаем сервер
exec gunicorn NeonDrive.wsgi:application