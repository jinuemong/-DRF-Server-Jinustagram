from .models import User
from django.db.models.signals import post_save
#유저 객체 생성 시 시그널 정보를 전달 
from django.dispatch import receiver
from user.models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance,created, **kwargs):
    
    if created:
        Profile.objects.create(username=instance)