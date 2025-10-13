import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# ✅ Configurer Django avant tout import
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AMOURECK.settings")

django_asgi_app = get_asgi_application()

from apps.chat import routing as chat_routing  # après init

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(chat_routing.websocket_urlpatterns)
    ),
})
