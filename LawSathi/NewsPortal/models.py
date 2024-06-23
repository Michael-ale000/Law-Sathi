from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MoreUserInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.BigIntegerField(blank=True,null=True)
    gender = models.CharField(max_length=6, blank=True , null=True)
    dob = models.DateField(blank=True,null=True)
    is_completed_for_lawyer = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username