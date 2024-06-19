# Generated by Django 5.0.6 on 2024-06-19 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LawyerRecommendation', '0003_alter_lawyerdetails_permanent_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='lawyerdetails',
            name='Rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='lawyerdocuments',
            name='citizenship_document',
            field=models.FileField(upload_to='documents/lcitizenship_document/'),
        ),
        migrations.AlterField(
            model_name='lawyerdocuments',
            name='license_certificate',
            field=models.FileField(upload_to='documents/license_certificates/'),
        ),
    ]