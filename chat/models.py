from django.db import models
from django.contrib.auth.models import User
import uuid


class UserList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100)
    userlist_id = models.CharField(default=uuid.uuid4, max_length=100)

    def __str__(self):
        return str(self.user)


class RoomChat(models.Model):
    name = models.CharField(max_length=20, unique=True)
    admin = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    room_id = models.CharField(default=uuid.uuid4, max_length=100)

    def __str__(self):
        return self.name


class AddUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(RoomChat, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.room}'


class Chat(models.Model):
    userlist_id1 = models.CharField(max_length=100)
    userlist_id2 = models.CharField(max_length=100)
    chat_id = models.CharField(default=uuid.uuid4, max_length=100)

    def __str__(self):
        return f'{self.chat_id}'


class Messages(models.Model):
    private_chat = models.ForeignKey(
        Chat, models.CASCADE, blank=True, null=True)
    room_chat = models.ForeignKey(
        RoomChat, models.CASCADE, blank=True, null=True)
    messages = models.CharField(max_length=200)
    documents = models.FileField(default='documents/')
    user = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.user} - {self.messages}'
