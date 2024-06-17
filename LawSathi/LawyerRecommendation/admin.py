from django.contrib import admin
from django.core.mail import send_mail
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from NewsPortal.models import MoreUserInfo
from .models import Address,LawyerDetails,LawyerDocuments
# Register your models here.
class MoreUserInfoInline(admin.StackedInline):
    model = MoreUserInfo
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (MoreUserInfoInline,)

class LawyerDetailsAdmin(admin.ModelAdmin):
    list_display = ['user', 'status']
    list_filter = ['status']

    def save_model(self, request, obj, form, change):
        # Get the previous status before saving changes
        prev_status = obj.status

        # Save the changes to the LawyerDetails model
        super().save_model(request, obj, form, change)

        # Check if status changed and send email
        if prev_status != obj.status:
            # Send email to lawyer
            subject = f"Status Updated: {obj.status}"
            message = f"Your lawyer application status has been updated to {obj.status}."
            from_email = "your@email.com"  # Set your from email address
            to_email = obj.user.email  # Get the lawyer's email from the related User model
            send_mail(subject, message, from_email, [to_email])

admin.site.unregister(User)
admin.site.register(User,UserAdmin)
admin.site.register(Address)
admin.site.register(LawyerDetails, LawyerDetailsAdmin)
admin.site.register(LawyerDocuments)