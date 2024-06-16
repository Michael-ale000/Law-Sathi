from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import MoreUserInfo

# Register your models here.
class MoreUserInfoInline(admin.StackedInline):
    model = MoreUserInfo
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (MoreUserInfoInline,)

admin.site.unregister(User)
admin.site.register(User,UserAdmin)