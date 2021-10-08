from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import ChatRoom
# Create your views here.
from django.contrib.auth.decorators import login_required


@login_required
def index_view(request):
    if request.method == 'POST':
        new_room_name = request['new_room_name']
        print(new_room_name)
        created_room = ChatRoom.create(room_name, request.user.id)
        ChatRoom.objects.add(created_room)
        return redirect('/chat')
    userdb = User.objects.get(pk=request.user.id)
    return render(request, 'chat/index.html', {'userdb': userdb})


@login_required
def room_view(request, room_id):
    room = ChatRoom.objects.get(pk=room_id)
    user_has_access = room.room_users.filter(pk=request.user.id).exists()
    if user_has_access:
        return render(request, 'chat/room.html', {
            'room': room,
        })
    else:
        return redirect('/chat')


def create_room_view(request, room_name):
    created_room = ChatRoom.create(room_name, request.user.id)
    ChatRoom.objects.add(created_room)
    return redirect('/chat')


# def login(request):
#     return render(request, 'chat/login.html', {})
