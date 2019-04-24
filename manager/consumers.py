# manager/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer

from home import models
from home.cart import update_data

class UpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "manager"
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = []
        bills = models.Bill.objects.all()
        for bill in bills:
            if not bill.finished:
                data.append({'id': bill.id, 'creation_date': bill.creation_date.strftime("%d-%m-%Y %H:%M:%S")})

        await self.send(text_data=json.dumps({
            'message': data
        }))

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
