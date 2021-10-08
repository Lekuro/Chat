from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import ChatRoom
# Create your views here.
from django.contrib.auth.decorators import login_required


@login_required
def index_view(request):
    if request.method == 'POST':
        new_room_name = request.POST['new_room_name']
        ChatRoom.create(new_room_name, request.user.id)
        return redirect('/chat')
    userdb = User.objects.get(pk=request.user.id)
    return render(request, 'chat/index.html', {'userdb': userdb})


@login_required
def room_view(request, room_id):
    room = ChatRoom.objects.get(pk=room_id)
    # not_invited_users = User.objects.all()
    not_invited_users = []
    for user in User.objects.all():
        if not user.chat_rooms.filter(id=room_id).exists():
            not_invited_users.append(user)
    user_has_access = room.room_users.filter(pk=request.user.id).exists()
    if user_has_access:
        return render(request, 'chat/room.html', {
            'room': room,
            'not_invited_users': not_invited_users
        })
    else:
        return redirect('/chat')


def invite_user(request, room_id):
    invited_user_id = request.POST['invited_user_id']
    invited_user = User.objects.get(id=invited_user_id)
    room = ChatRoom.objects.get(id=room_id)
    if not room.room_users.filter(id=invited_user_id).exists():
        room.room_users.add(invited_user)
    return redirect('/chat')
