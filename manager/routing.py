# manager/routing.py
from django.conf.urls import url
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/manager/', consumers.UpdateConsumer),
]