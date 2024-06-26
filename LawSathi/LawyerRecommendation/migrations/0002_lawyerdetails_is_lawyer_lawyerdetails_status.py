# Generated by Django 5.0.6 on 2024-06-17 06:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("LawyerRecommendation", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="lawyerdetails",
            name="is_lawyer",
            field=models.BooleanField(default=True, editable=False),
        ),
        migrations.AddField(
            model_name="lawyerdetails",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("approved", "Approved"),
                    ("rejected", "Rejected"),
                ],
                default="pending",
                max_length=10,
            ),
        ),
    ]
