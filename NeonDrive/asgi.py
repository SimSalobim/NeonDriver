import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import main.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NeonDrive.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        main.routing.websocket_urlpatterns
    ),
})