from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import ChatRoom
from django.contrib.auth.decorators import login_required


@login_required
def index_view(request):
    # userdb = User.objects.get(pk=request.user.id)
    userdb = get_object_or_404(User, pk=request.user.id)
    if request.method == 'POST':
        #new_room_name = request.POST['new_room_name']
        new_room_name = request.POST.get('new_room_name', False)
        if new_room_name:
            print(userdb.chat_rooms)
            if ChatRoom.objects.filter(room_name=new_room_name).exists():
                return render(request, 'chat/index.html', {'userdb': userdb, 'error_message': f'Room {new_room_name} alredy exists'})
            r = ChatRoom.create(new_room_name, request.user.id)
            print('was created room:', r)
            if not r:
                return render(request, 'chat/index.html',
                              {'userdb': userdb, 'error_message': "Room wasn't created"})
        return redirect('/chat')
    return render(request, 'chat/index.html', {'userdb': userdb})


@login_required
def room_view(request, room_id):
    # room = ChatRoom.objects.get(pk=room_id)
    room = get_object_or_404(ChatRoom, pk=room_id)
    user_has_access = room.room_users.filter(pk=request.user.id).exists()
    if not user_has_access:
        return redirect('/chat')
    # for user in User.objects.all():
    #     if not user.chat_rooms.filter(id=room_id).exists():
    #         not_invited_users.append(user)
    #     else:
    #         room_users.append(user)
    room_users = room.room_users
    room_user_ids = list(room_users.values_list('id', flat=True))
    not_invited_users = User.objects.exclude(id__in=room_user_ids)
    return render(request, 'chat/room.html', {
        'room': room,
        'not_invited_users': not_invited_users,
        'room_users': room_users,
    })


def invite_user(request, room_id):
    # invited_user_id = request.POST['invited_user_id']
    invited_user_id = request.POST.get('invited_user_id', False)
    # invited_user = User.objects.get(id=invited_user_id)
    invited_user = get_object_or_404(User, pk=invited_user_id)
    room = ChatRoom.objects.get(id=room_id)
    if not room.room_users.filter(id=invited_user_id).exists():
        room.room_users.add(invited_user)
    return redirect(f'/chat/{room_id}')


def redirect_to_chat(request):
    return redirect('/chat')
