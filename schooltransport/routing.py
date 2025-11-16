"""
WebSocket URL routing for Django Channels
Defines WebSocket endpoints for real-time communication
"""

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Notification consumer - for receiving real-time notifications
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),

    # Bus tracking consumer - for live GPS tracking
    re_path(r'ws/bus/(?P<bus_id>\w+)/tracking/$', consumers.BusTrackingConsumer.as_asgi()),

    # Student check-in consumer - for attendance tracking
    re_path(r'ws/bus/(?P<bus_id>\w+)/checkin/$', consumers.StudentCheckinConsumer.as_asgi()),
]
