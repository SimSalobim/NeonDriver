import os
import django  # Добавьте этот импорт
from django.core.asgi import get_asgi_application

# Важно: сначала установить переменные окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NeonDrive.settings')
django.setup()  # Теперь это будет работать корректно

# Затем импортировать остальные модули
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import main.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            main.routing.websocket_urlpatterns
        )
    ),
})