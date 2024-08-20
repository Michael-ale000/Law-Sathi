from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()
class FileUpload(models.Model):
    file = models.FileField(upload_to='documents/law_pdfs')
    name = models.CharField(max_length=255, blank=False)
    uploaded_by = models.ForeignKey(User , on_delete=models.CASCADE)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255,blank=True)

    def __str__(self):
        return self.file.name
    