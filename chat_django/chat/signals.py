from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import ChatRoom


@receiver(post_save, sender=ChatRoom)
def post_save_user(created, instance, **kwargs):
    if created and instance.creator:
        instance.room_users.add(instance.creator)
