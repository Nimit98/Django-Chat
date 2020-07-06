from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Messages, RoomChat, Chat, AddUser, Notification, UserList, NotificationPrivate
import datetime
from django.contrib.auth.models import User


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

    def notification(self, chat_id, label, user, c):
        current = UserList.objects.get(user__username=user)
        if label == 'room':
            users = AddUser.objects.filter(
                room__room_id=chat_id).exclude(user__username=user)
            for u in users:
                try:
                    exist = Notification.objects.get(user=u.user, room_chat=c)
                    exist.new_message = True
                    exist.count += 1
                    exist.save()
                except:
                    new = Notification(user=u.user, room_chat=c)
                    new.new_message = True
                    new.count += 1
                    new.save()
        elif label == 'private':
            if c.userlist_id1 == current.userlist_id:
                opp = c.userlist_id2
            else:
                opp = c.userlist_id1
            opp = UserList.objects.get(userlist_id=opp)
            try:
                exist = NotificationPrivate.objects.get(
                    sender=current, receiver=opp.user)
                exist.new_message = True
                exist.count += 1
                exist.save()
            except:
                new = NotificationPrivate(sender=current, receiver=opp.user)
                new.new_message = True
                new.count += 1
                new.save()

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
            self.notification(chat_id, label, user, c)
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
