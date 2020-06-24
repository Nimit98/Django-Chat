from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Messages, RoomChat, Chat
import datetime


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def messages_to_json(self, messages, chat_id):
        result = []
        for message in messages:
            result.append(self.message_to_json(message, chat_id))
        return result

    def message_to_json(self, message, chat_id):

        time = str(message.time)
        time = time[:5]
        return {
            'user': message.user,
            'content': message.messages,
            'chat_id': chat_id,
            'time': time,
            'date': str(message.date)
        }

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']
        chat_id = text_data_json['chat_id']
        user = text_data_json['user']
        try:
            c = Chat.objects.get(chat_id=chat_id)
            label = 'private'
        except Chat.DoesNotExist:
            c = RoomChat.objects.get(room_id=chat_id)
            label = 'room'

        # FETCH MESSAGES
        if command == 'fetch messages':
            print(chat_id)
            if label == 'private':
                messages = Messages.objects.filter(
                    private_chat__chat_id=chat_id)
            elif label == 'room':
                messages = Messages.objects.filter(room_chat__room_id=chat_id)
            content = {
                'state': 'fetched_messages',
                'user': user,
                'label': label,
                'messages': self.messages_to_json(messages, chat_id)
            }
            self.send_message(content)

        # SAVE MESSAGES
        else:
            print(chat_id, 'tt')
            message = text_data_json['message']
            user = text_data_json['user']
            if label == 'private':
                new_message = Messages(
                    user=user, private_chat=c, messages=message)
            elif label == 'room':
                new_message = Messages(
                    user=user, room_chat=c, messages=message)
            new_message.save()

            time = str(datetime.datetime.now())
            [date, time] = time.split(" ")
            time = time[:5]

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': user,
                    'label': label,
                    'state': 'sent_message',
                    'time': time,
                }
            )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        user = event['user']
        state = event['state']
        label = event['label']
        time = event['time']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'state': state,
            'user': user,
            'label': label,
            'time': time
        }))

    def send_message(self, message):
        self.send(text_data=json.dumps(message))
