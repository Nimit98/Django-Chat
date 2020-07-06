from django.contrib import admin

from .models import UserList, Chat, Messages, RoomChat, AddUser, Notification, NotificationPrivate

admin.site.register(UserList)
admin.site.register(Chat)
admin.site.register(Messages)
admin.site.register(RoomChat)
admin.site.register(AddUser)
admin.site.register(Notification)
admin.site.register(NotificationPrivate)
