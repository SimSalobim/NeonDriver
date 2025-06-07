import os
import django
from django.core.asgi import get_asgi_application
from channels.layers import get_channel_layer
import logging

logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NeonDrive.settings')
django.setup()

try:
    channel_layer = get_channel_layer()
    logger.info(f"Channel layer initialized: {channel_layer}")

    # Проверка соединения с Redis
    if hasattr(channel_layer, 'connection'):
        conn = channel_layer.connection()
        conn.ping()
        logger.info("Redis connection successful!")

except Exception as e:
    logger.error(f"Error initializing channel layer: {str(e)}")
    import traceback

    logger.error(traceback.format_exc())