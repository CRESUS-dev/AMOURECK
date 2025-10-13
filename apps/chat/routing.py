from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # ws://<host>/ws/chat/<room>/
    re_path(r"^ws/chat/(?P<room>[^/]+)/$", consumers.ChatConsumer.as_asgi()),
]
