import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import main.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NeonDrive.settings')

# Добавлен вызов миграций для ASGI
try:
    from startup import run_migrations
    run_migrations()
except ImportError as e:
    print(f"Startup import error: {e}")
except Exception as e:
    print(f"Initialization error: {e}")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            main.routing.websocket_urlpatterns
        )
    ),
})