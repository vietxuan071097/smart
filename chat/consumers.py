# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.sessions.models import Session

from chat.models import Message, Conversation


def fetch_messages(ID):
    messages = Message.objects.filter(conversation_id=ID)
    return messages


def message_to_json(message):
    return json.dumps({
        'type': 'chat_message',
        'author': message.author.session_key,
        'to': str(message.conversation_id),
        'message': message.content
    })


class ChatConsumer(AsyncWebsocketConsumer):
    commands = {
        'fetch_messages', fetch_messages
    }

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.session_key = self.scope['session'].session_key
        self.session = Session.objects.get(session_key=self.session_key)
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
        text_data_json = json.loads(text_data)

        if text_data_json['command'] == "fetch_messages":
            for message in fetch_messages(text_data_json['ID']):
                await self.send(text_data=message_to_json(message))
        else:
            message = text_data_json['message']
            author = text_data_json['from']
            to = text_data_json['to']
            Message.objects.create(author_id=author, content=message, conversation_id=to)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'author': author,
                    'to': to
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        author = event['author']
        to = event['to']

        if self.session in Conversation.objects.get(id=to).member.all():
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'message': message,
                'author': author,
                'to': event['to']
            }))
