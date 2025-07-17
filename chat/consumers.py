from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Message
from .serializers import MessageSerializer
import json
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            await self.close()
            return
        self.recipient_id = self.scope['url_route']['kwargs']['recipient_id']
        self.room_group_name = f'chat_{min(self.user.id, int(self.recipient_id))}_{max(self.user.id, int(self.recipient_id))}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        recipient_id = self.recipient_id

        # Save message to database
        message_obj = await self.save_message(self.user.id, recipient_id, message)
        serialized_message = await self.serialize_message(message_obj)

        # Broadcast message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': serialized_message,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message']))

    @database_sync_to_async
    def save_message(self, sender_id, recipient_id, content):
        return Message.objects.create(
            sender_id=sender_id,
            recipient_id=recipient_id,
            content=content
        )

    @database_sync_to_async
    def serialize_message(self, message):
        return MessageSerializer(message).data