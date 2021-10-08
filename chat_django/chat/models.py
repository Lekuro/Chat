from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ChatRoom(models.Model):
    room_name = models.CharField(unique=True, max_length=255)
    # creator = models.ForeignKey(User, on_delete=models.RESTRICT)
    room_users = models.ManyToManyField(User, related_name='chat_rooms')

    def __str__(self):
        return self.room_name

    def create(self, room_name, user_id):
        self.room_name = room_name
        user_room_creator = User.objects.get(pk=user_id)
        self.room_users.add(user_room_creator)
        return self
