import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from espdata.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Xử lý HTTP request
    "websocket": AuthMiddlewareStack(  # Xử lý WebSocket
        URLRouter(websocket_urlpatterns)
    ),
})
