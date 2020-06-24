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
    print(room_name, 'roomihh')
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
        return render(request, 'chat/room.html', {
            'room_id': room_name,
            'chat_name': chat_name,
            'group': 'private',
        })
    except Chat.DoesNotExist:

        users = AddUser.objects.filter(room__room_id=room_name)
        print(users)
        room = users[0].room.name
        roomId = users[0].room.id
        if request.user == users[0].room.admin:
            admin = True
        else:
            admin = False
        print(room_name, 'll')
        chat_name = room
        return render(request, 'chat/room.html', {
            'room_id': room_name,
            'chat_name': chat_name,
            'group': 'room',
            'users': users,
            'admin': admin,
            'roomId': roomId
        })


@ csrf_exempt
def create_room(request):
    roomName = request.POST.get('room')
    room = RoomChat(name=roomName, admin=request.user)
    room.save()
    new_user = AddUser(user=request.user, room=room)
    new_user.save()
    room = RoomChat.objects.get(id=room.id)
    room_id = room.room_id[:7]
    room.room_id = room_id
    room.save()
    return HttpResponse(json.dumps({'room': room_id}), content_type='application/json')


@ csrf_exempt
def room_id(request):
    roomid = request.POST.get('room')
    room_name = request.POST.get('room_name')

    print(roomid, 'jjjj')
    room = RoomChat.objects.get(room_id=roomid)
    return HttpResponseRedirect(reverse('chat:room', args=(roomid,)))


def add_users(request, pk):
    # ad = AddUser.objects.get(id=pk)
    # print(ad)
    added = AddUser.objects.filter(room=pk)
    room = added[0].room
    users = []
    for u in added:
        users.append(User.objects.get(username=u.user.username))
    print(users)
    to_add = UserList.objects.exclude(user__in=users)
    print(to_add)
    if request.method == 'POST':
        users = request.POST.getlist('users[]')
        for u in users:
            user = UserList.objects.get(id=u)
            add = AddUser(room=room, user=user.user)
            add.save()
        return HttpResponseRedirect(reverse('chat:index'))
    return render(request, 'chat/add_users.html', {'users': to_add})


def changeSettings(request):
    if 'name' in request.GET:
        if request.method == 'POST':
            name = request.POST.get('name')
            name = name.replace(" ", "")

            # Change name in messages
            messages = Messages.objects.filter(user=request.user.username)
            for message in messages:
                message.user = name
                message.save()

            user = UserList.objects.get(user__username=request.user.username)
            user.display_name = name
            user.save()
            user = User.objects.get(username=request.user.username)
            user.username = name
            user.save()

            return HttpResponseRedirect(reverse('index'))
        else:
            messages = Messages.objects.filter(user=request.user.username)
            print(messages)
            return render(request, 'chat/change.html', {'change': 'name'})


def delete(request, pk):
    if 'leave_room' in request.GET:
        room = AddUser.objects.get(id=pk)
        if request.method == 'POST':
            room.delete()
            return HttpResponseRedirect(reverse('chat:index'))
        return render(request, 'chat/delete_leave.html', {'status': 'leave'})
    if 'delete_room' in request.GET:
        room = AddUser.objects.get(id=pk)
        room = room.room
        if request.method == 'POST':
            room.delete()
            return HttpResponseRedirect(reverse('chat:index'))
        return render(request, 'chat/delete_leave.html', {'status': 'delete'})


def remove_user(request, pk):
    user = AddUser.objects.get(id=pk)
    room = user.room.room_id
    if request.method == 'POST':
        user.delete()
        return HttpResponseRedirect(reverse('chat:room', args=(room,)))
    return render(request, 'chat/remove_user.html', {'user': user})
