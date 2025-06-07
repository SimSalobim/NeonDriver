import os
from django.core.asgi import get_asgi_application
from django.template.backends import django

# Важно: сначала установить переменные окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NeonDrive.settings')

# Затем импортировать остальные модули
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import main.routing

# Убедитесь, что приложение инициализируется после настроек
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NeonDrive.settings')
django.setup()  # Добавьте эту строку

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(main.routing.websocket_urlpatterns)
    ),
})