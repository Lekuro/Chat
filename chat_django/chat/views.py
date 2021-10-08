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
    user_has_access = room.room_users.filter(pk=request.user.id).exists()
    if user_has_access:
        return render(request, 'chat/room.html', {
            'room': room,
        })
    else:
        return redirect('/chat')
