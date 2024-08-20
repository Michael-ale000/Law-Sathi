from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()
class FileUploads(models.Model):
    file = models.FileField(upload_to='documents/law_pdfs')
    name = models.CharField(max_length=255, blank=False)
    uploaded_by = models.ForeignKey(User , on_delete=models.CASCADE)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255,blank=True)

    def __str__(self):
        return self.file.name
    
# model for unknown query 
class UnknownQuerys(models.Model):
    user_query = models.TextField()
    bot_responses = models.TextField()
    bot_querytimestamp = models.DateTimeField(auto_now_add=True)
    handled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_query[:50]}(Handled:{self.handled})"
    
