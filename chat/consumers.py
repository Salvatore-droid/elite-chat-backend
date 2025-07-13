from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Message
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.recipient_id = self.scope['url_route']['kwargs']['recipient_id']
        self.room_group_name = f'chat_{min(self.user.id, int(self.recipient_id))}_{max(self.user.id, int(self.recipient_id))}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        recipient_id = self.recipient_id

        # Save message to database
        await self.save_message(self.user.id, recipient_id, message)

        # Broadcast message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': self.user.id,
                'recipient_id': recipient_id,
                'timestamp': str(Timezone.now()),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
            'recipient_id': event['recipient_id'],
            'timestamp': event['timestamp'],
        }))

    @database_sync_to_async
    def save_message(self, sender_id, recipient_id, content):
        Message.objects.create(
            sender_id=sender_id,
            recipient_id=recipient_id,
            content=content
        )