import os
import django
import logging
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import main.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NeonDrive.settings')
django.setup()

logger = logging.getLogger(__name__)
logger.info("ASGI application initialized")

# Проверим инициализацию канального слоя
from channels.layers import get_channel_layer
try:
    channel_layer = get_channel_layer()
    logger.info(f"Channel layer initialized: {channel_layer}")
except Exception as e:
    logger.error(f"Error initializing channel layer: {str(e)}")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            main.routing.websocket_urlpatterns
        )
    ),
})