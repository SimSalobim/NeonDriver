import os
import django
import logging
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NeonDrive.settings')
django.setup()

logger = logging.getLogger(__name__)
logger.info("ASGI application initialized")

# Проверим инициализацию канального слоя
from channels.layers import get_channel_layer
from django.conf import settings

try:
    channel_layer = get_channel_layer()
    logger.info(f"Channel layer initialized: {channel_layer}")

    # Проверим конфигурацию
    logger.info(f"Channel layer config: {settings.CHANNEL_LAYERS}")
except Exception as e:
    logger.error(f"Error initializing channel layer: {str(e)}")
    import traceback

    logger.error(traceback.format_exc())

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