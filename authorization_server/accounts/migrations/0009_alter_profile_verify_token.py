# Generated by Django 4.0.5 on 2022-06-26 05:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_profile_verify_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='verify_token',
            field=models.CharField(default=uuid.UUID('ac15ab47-f740-49ac-92ee-b6d6fc94ba3c'), max_length=255, null=True),
        ),
    ]
