from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your laywer models here.

#Laywaer address
class Address(models.Model):
    province =  models.CharField(max_length=100)
    district =  models.CharField(max_length=100)
    location =  models.CharField(max_length=100)

    def __str__(self):
        return f"{self.location}, {self.district}, {self.province}"
    

#laywaer details
class LawyerDetails(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    experience = models.PositiveIntegerField(help_text="Years of experience")
    bar_license = models.CharField(max_length=100, unique=True)
    average_case_completion_days = models.PositiveIntegerField()
    permanent_address = models.CharField(max_length=255)
    office_address = models.OneToOneField(Address, related_name='office_address', on_delete=models.CASCADE)
    is_lawyer = models.BooleanField(default=True, editable=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"{self.user.username} - {self.bar_license}"

#lawyer documents
class LawyerDocuments(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    license_certificate = models.FileField(upload_to='documents/license_certificates/')
    citizenship_document = models.FileField(upload_to='documents/lcitizenship_document/')
    personal_photos = models.ImageField(upload_to='documents/personal_photos/')

    def __str__(self):
        return f"Dcouments of {self.user.username}"