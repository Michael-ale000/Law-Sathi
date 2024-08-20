from django.contrib import admin
from .models import FileUpload

# Register your models here.

# file upload admin

class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('name','file','uploaded_by','uploaded_date', 'description')
    search_fields = ('name', 'description')
    readonly_fields = ('uploaded_date', 'uploaded_by')  # Make these fields read-only

    def save_model(self,request,obj,form,change):
        if not obj.pk:
            obj.uploaded_by = request.user
        super().save_model(request,obj,form,change)

admin.site.register(FileUpload,FileUploadAdmin)