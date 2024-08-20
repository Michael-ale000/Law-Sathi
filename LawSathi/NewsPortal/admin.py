from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import MoreUserInfo
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from LawyerRecommendation.models import LawyerDetails

# Register your models here.
class MoreUserInfoInline(admin.StackedInline):
    model = MoreUserInfo
    can_delete = False

# for filtering the types of users
User = get_user_model()

# Define the custom filter
class UserTypeFilter(admin.SimpleListFilter):
    title = _('User Type')
    parameter_name = 'user_type'

    def lookups(self, request, model_admin):
        return (
            ('general', _('General Users')),
            ('lawyers', _('Lawyers')),
            ('staff', _('Staff')),
            ('superuser', _('Superuser')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'general':
            return queryset.filter(is_staff=False, is_superuser=False).exclude(id__in=LawyerDetails.objects.values('user_id'))
        if self.value() == 'lawyers':
            return queryset.filter(id__in=LawyerDetails.objects.values('user_id'))
        if self.value() == 'staff':
            return queryset.filter(is_staff=True, is_superuser=False)
        if self.value() == 'superuser':
            return queryset.filter(is_superuser=True)
        return queryset
    

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_lawyer', 'is_staff', 'is_superuser')
    list_filter = (UserTypeFilter,)  # Add the custom filter here
    search_fields = ('username', 'email', 'first_name', 'last_name')
    inlines = (MoreUserInfoInline,)
    def is_lawyer(self, obj):
        # Check if there is a related LawyerDetails entry
        return LawyerDetails.objects.filter(user=obj).exists()
    is_lawyer.boolean = True  # Display as a boolean icon in the admin list view
    is_lawyer.short_description = 'Is Lawyer'

admin.site.unregister(User)
admin.site.register(User,UserAdmin)