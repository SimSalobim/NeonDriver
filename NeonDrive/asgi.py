import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NeonDrive.settings')

# Инициализируем Django перед импортом зависимостей
django_application = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from main.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_application,
    "websocket": URLRouter(
        websocket_urlpatterns
    ),
})