from django.shortcuts import render
from .models import UserList, Chat, Messages, RoomChat, AddUser
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import time
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json


@login_required(login_url='/login/')
def index(request):
    if request.method == 'GET':
        users = UserList.objects.exclude(user__username=request.user.username)
        rooms = AddUser.objects.filter(user__username=request.user.username)
        return render(request, 'chat/index.html', {'users': users, 'rooms': rooms})


def get_id(request, pk):
    receiver_user = UserList.objects.all().get(id=pk)
    receiver_user_id = receiver_user.userlist_id
    sent_user = UserList.objects.all().get(user=request.user)
    sent_user_id = sent_user.userlist_id
    try:
        chat = Chat.objects.get(userlist_id1=sent_user_id,
                                userlist_id2=receiver_user_id)
        chat_id = chat.chat_id
    except Chat.DoesNotExist:
        try:
            chat = Chat.objects.get(userlist_id2=sent_user_id,
                                    userlist_id1=receiver_user_id)
            chat_id = chat.chat_id
        except Chat.DoesNotExist:
            chat = Chat(userlist_id1=sent_user_id,
                        userlist_id2=receiver_user_id)
            chat.save()
            chat = Chat.objects.get(userlist_id1=sent_user_id,
                                    userlist_id2=receiver_user_id)
            chat_id = chat.chat_id[:7]
            chat.chat_id = chat_id
            chat.save()
    c = chat_id[:7]
    return HttpResponseRedirect(reverse('chat:room', args=(c,)))


def room(request, room_name):
    try:
        opposite_user = Chat.objects.get(chat_id=room_name)
        user = UserList.objects.get(user__username=request.user.username)
        userid = user.userlist_id
        if userid == opposite_user.userlist_id1:
            chat_name = UserList.objects.get(
                userlist_id=opposite_user.userlist_id2)
            chat_name = chat_name.user.username
        else:
            chat_name = UserList.objects.get(
                userlist_id=opposite_user.userlist_id1)
            chat_name = chat_name.user.username
    except:
        chat_name = room_name
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'chat_name': chat_name
    })


@ csrf_exempt
def room_id(request):
    room_name = str(request.POST.get('room'))
    if room_name != 'None':
        try:
            room = RoomChat.objects.get(name=room_name)
            room_id = room.room_id[:7]
            print('exist')
            try:
                exist = AddUser.objects.get(
                    user__username=request.user.username, room=room)
                return HttpResponseRedirect(reverse('chat:room', args=(room_id,)))
            except AddUser.DoesNotExist:
                user = User.objects.get(username=request.user.username)
                new_user = AddUser(user=user, room=room)
                new_user.save()
                return HttpResponseRedirect(reverse('chat:room', args=(room_id,)))

        except RoomChat.DoesNotExist:
            room = RoomChat(name=room_name)
            room.save()
            user = User.objects.get(username=request.user.username)
            new_user = AddUser(user=user, room=room)
            new_user.save()
            room = RoomChat.objects.get(name=room_name)
            room_id = room.room_id[:7]
            room.room_id = room_id
            room.save()
            return HttpResponseRedirect(reverse('chat:room', args=(room_id,)))
    else:
        return HttpResponseRedirect(reverse('chat:index'))


def changeSettings(request):
    if 'name' in request.GET:
        if request.method == 'POST':
            name = request.POST.get('name')
            user = UserList.objects.get(user__username=request.user.username)
            user.display_name = name
            user.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'chat/change.html', {'change': 'name'})
