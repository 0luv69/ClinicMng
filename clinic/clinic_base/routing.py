from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # e.g. ws://<host>/ws/chat/123/
    re_path(r"^ws/chat/(?P<conversation_id>\d+)/$", consumers.ChatConsumer.as_asgi()),

     # Clients connect to ws://…/ws/webrtc/<room_name>/
    re_path(r'ws/webrtc/(?P<room_name>\w+)/$', consumers.SignalingConsumer.as_asgi()),
]