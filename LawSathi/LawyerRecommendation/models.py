from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.template.loader import render_to_string
# Create your laywer models here.

#Laywaer address
class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    province =  models.CharField(max_length=99)
    district =  models.CharField(max_length=100)
    location =  models.CharField(max_length=100)

    def __str__(self):
            return f"Address-{self.user.username}"
    

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
        if self.user_id:
            return f"{self.user.username}"
        return f"LawyerDetails - {self.bar_license}"

#lawyer documents
class LawyerDocuments(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    license_certificate = models.FileField(upload_to='documents/license_certificates/')
    citizenship_document = models.FileField(upload_to='documents/lcitizenship_document/')
    personal_photos = models.ImageField(upload_to='documents/personal_photos/')

    def __str__(self):
        return f"Dcouments of {self.user.username}"
    
@receiver(post_save, sender=LawyerDetails)
def accept_or_reject_email(sender, instance, created, **kwargs):
    # print(instance.user)
    if instance.status == 'rejected':
        subject = 'Sorry! Your form has been rejected'
        html_message = render_to_string('reject_emailtemplate.html', {'lawyer_name': instance.user.username})
        plain_message = strip_tags(html_message)
        from_email = 'your_email@gmail.com'  # Sender email address
        to_email = instance.user.email  # Lawyer's email address
        send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
        User.objects.get(username=instance.user).delete()
    if instance.status == 'approved':  # Check if status is 'approved'
        subject = 'Congratulations! Your form has been accepted'
        html_message = render_to_string('approved_emailtemplate.html', {'lawyer_name': instance.user.username})
        plain_message = strip_tags(html_message)
        from_email = 'your_email@gmail.com'  # Sender email address
        to_email = instance.user.email  # Lawyer's email address
        send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)