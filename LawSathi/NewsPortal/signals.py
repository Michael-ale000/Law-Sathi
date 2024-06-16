from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import MoreUserInfo

@receiver(post_save, sender=User)
def create_or_update_mpreuserinfo(sender,instance,created,**kwargs):
    if created:
        MoreUserInfo.objects.create(user=instance)
    else:
        instance.moreuserinfo.save()