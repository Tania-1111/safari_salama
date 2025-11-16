"""
WebSocket consumers for real-time communication
Handles live notifications and GPS updates
"""

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
import logging

logger = logging.getLogger(__name__)


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time notifications
    Sends live updates to guardians about their students
    """

    async def connect(self):
        """Accept WebSocket connection"""
        self.user_id = self.scope['user'].id
        self.user_group_name = f'user_{self.user_id}'

        # Add to group
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )

        await self.accept()
        logger.info(f"User {self.user_id} connected to notifications")

    async def disconnect(self, close_code):
        """Remove from group on disconnect"""
        await self.channel_layer.group_discard(
            self.user_group_name,
            self.channel_name
        )
        logger.info(f"User {self.user_id} disconnected from notifications")

    async def receive(self, text_data):
        """Receive message from WebSocket"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')

            if message_type == 'notification':
                # Broadcast notification to group
                await self.channel_layer.group_send(
                    self.user_group_name,
                    {
                        'type': 'send_notification',
                        'title': data.get('title'),
                        'message': data.get('message'),
                        'timestamp': data.get('timestamp'),
                    }
                )
        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
        except Exception as e:
            logger.error(f"Error in receive: {e}")

    async def send_notification(self, event):
        """
        Send notification to WebSocket
        Called by group_send
        """
        notification = {
            'type': 'notification',
            'title': event['title'],
            'message': event['message'],
            'timestamp': event['timestamp'],
        }

        # Send notification to WebSocket
        await self.send(text_data=json.dumps(notification))


class BusTrackingConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time bus tracking
    Updates guardians with live bus location
    """

    async def connect(self):
        """Accept WebSocket connection"""
        self.bus_id = self.scope['url_route']['kwargs'].get('bus_id')
        self.user_id = self.scope['user'].id
        self.bus_group_name = f'bus_{self.bus_id}'

        # Add to bus tracking group
        await self.channel_layer.group_add(
            self.bus_group_name,
            self.channel_name
        )

        await self.accept()
        logger.info(f"User {self.user_id} tracking bus {self.bus_id}")

    async def disconnect(self, close_code):
        """Remove from group on disconnect"""
        await self.channel_layer.group_discard(
            self.bus_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Receive GPS location from driver"""
        try:
            data = json.loads(text_data)

            if data.get('type') == 'location_update':
                # Broadcast location to all users tracking this bus
                await self.channel_layer.group_send(
                    self.bus_group_name,
                    {
                        'type': 'location_update',
                        'bus_id': self.bus_id,
                        'latitude': data.get('latitude'),
                        'longitude': data.get('longitude'),
                        'speed': data.get('speed'),
                        'heading': data.get('heading'),
                        'timestamp': data.get('timestamp'),
                    }
                )

                # Save to database
                await self.save_bus_location(
                    self.bus_id,
                    data.get('latitude'),
                    data.get('longitude'),
                    data.get('speed'),
                    data.get('heading'),
                    data.get('accuracy')
                )
        except Exception as e:
            logger.error(f"Error in receive: {e}")

    async def location_update(self, event):
        """Send location update to WebSocket"""
        location = {
            'type': 'location_update',
            'bus_id': event['bus_id'],
            'latitude': event['latitude'],
            'longitude': event['longitude'],
            'speed': event['speed'],
            'heading': event['heading'],
            'timestamp': event['timestamp'],
        }

        await self.send(text_data=json.dumps(location))

    @database_sync_to_async
    def save_bus_location(self, bus_id, latitude, longitude, speed, heading, accuracy):
        """Save bus location to database"""
        from .models import Bus, BusLocation

        try:
            bus = Bus.objects.get(id=bus_id)
            BusLocation.objects.create(
                bus=bus,
                latitude=latitude,
                longitude=longitude,
                speed=speed,
                heading=heading,
                accuracy=accuracy
            )
            # Update bus current location
            bus.current_latitude = latitude
            bus.current_longitude = longitude
            bus.save()
        except Bus.DoesNotExist:
            logger.error(f"Bus {bus_id} not found")
        except Exception as e:
            logger.error(f"Error saving location: {e}")


class StudentCheckinConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for student check-in/out events
    Notifies guardians when student boards/alights
    """

    async def connect(self):
        """Accept WebSocket connection"""
        self.bus_id = self.scope['url_route']['kwargs'].get('bus_id')
        self.attendant_group_name = f'bus_attendant_{self.bus_id}'

        await self.channel_layer.group_add(
            self.attendant_group_name,
            self.channel_name
        )

        await self.accept()
        logger.info(f"Attendant connected to bus {self.bus_id}")

    async def disconnect(self, close_code):
        """Remove from group on disconnect"""
        await self.channel_layer.group_discard(
            self.attendant_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Receive student check-in/out data"""
        try:
            data = json.loads(text_data)

            if data.get('type') in ['student_boarded', 'student_alighted']:
                # Broadcast to all attendants on this bus
                await self.channel_layer.group_send(
                    self.attendant_group_name,
                    {
                        'type': data.get('type'),
                        'student_id': data.get('student_id'),
                        'student_name': data.get('student_name'),
                        'status': data.get('status'),
                        'timestamp': data.get('timestamp'),
                        'latitude': data.get('latitude'),
                        'longitude': data.get('longitude'),
                    }
                )

                # Send notification to guardian
                await self.notify_guardian(
                    data.get('student_id'),
                    data.get('student_name'),
                    data.get('status')
                )

        except Exception as e:
            logger.error(f"Error in receive: {e}")

    async def student_boarded(self, event):
        """Send student boarded notification"""
        notification = {
            'type': 'student_boarded',
            'student_name': event['student_name'],
            'status': 'boarded',
            'timestamp': event['timestamp'],
            'location': {
                'latitude': event['latitude'],
                'longitude': event['longitude'],
            }
        }
        await self.send(text_data=json.dumps(notification))

    async def student_alighted(self, event):
        """Send student alighted notification"""
        notification = {
            'type': 'student_alighted',
            'student_name': event['student_name'],
            'status': 'alighted',
            'timestamp': event['timestamp'],
            'location': {
                'latitude': event['latitude'],
                'longitude': event['longitude'],
            }
        }
        await self.send(text_data=json.dumps(notification))

    @database_sync_to_async
    def notify_guardian(self, student_id, student_name, status):
        """Create notification for guardian"""
        from .models import Student, Notification
        from django.utils import timezone

        try:
            student = Student.objects.get(id=student_id)
            guardian = student.guardian

            if guardian:
                if status == 'boarded':
                    message = f"{student_name} has boarded the bus"
                    notif_type = 'boarded'
                else:
                    message = f"{student_name} has alighted from the bus"
                    notif_type = 'alighted'

                Notification.objects.create(
                    recipient=guardian,
                    student=student,
                    notification_type=notif_type,
                    title='Student Transportation Alert',
                    message=message
                )
        except Exception as e:
            logger.error(f"Error notifying guardian: {e}")
