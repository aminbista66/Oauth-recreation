# Generated by Django 4.0.5 on 2022-06-21 08:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_profile_verify_token_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='verify_token',
            field=models.CharField(default=uuid.UUID('c7f19050-a36d-46bc-b576-b4f3d35563f0'), max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
