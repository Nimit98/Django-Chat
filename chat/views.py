from django.shortcuts import render
from .models import UserList, Chat, Messages, RoomChat, AddUser
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import time
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url='/login/')
def index(request):
    if request.method == 'GET':
        users = User.objects.exclude(username=request.user.username)
        return render(request, 'chat/index.html', {'users': users})


def get_id(request, pk):
    u = User.objects.all().get(pk=pk)
    receiver_user = UserList.objects.all().get(user=u)
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
            print('here')
    print(chat_id, 'here')
    c = chat_id[:7]
    return HttpResponseRedirect(reverse('chat:room', args=(c,)))


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


@csrf_exempt
def room_id(request):
    room_name = str(request.POST.get('room'))
    try:
        room = RoomChat.objects.get(name=room_name)
        room_id = room.room_id[:7]
        print('exist')
        return HttpResponseRedirect(reverse('chat:room', args=(room_id,)))
    except RoomChat.DoesNotExist:
        room = RoomChat(name=room_name)
        room.save()
        user = User.objects.get(username=request.user.username)
        print(user)
        new_user = AddUser(user=user, room=room)
        new_user.save()
        room = RoomChat.objects.get(name=room_name)
        room_id = room.room_id[:7]
        room.room_id = room_id
        room.save()
        return HttpResponseRedirect(reverse('chat:room', args=(room_id,)))
