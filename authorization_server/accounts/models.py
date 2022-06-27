from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .validators import validate_phone
from django.db.models.signals import post_save
import uuid 
import random

class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(max_length=10, default="9821152307", validators=[validate_phone])
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username",]
    
    def __str__(self) -> str:
        return f"{self.email}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False, blank=True, null=False)
    verify_token = models.CharField(max_length=255, blank=False, null=True, default=uuid.uuid4())

    def __str__(self) -> str:
        return f"{self.user.email}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.verify_token = uuid.uuid4()
        return super().save(force_insert, force_update, using, update_fields)

class OTP(models.Model):
    code = models.CharField(max_length=5, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        code = str(random.randint(10000, 99999))
        self.code = code
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self) -> str:
        return f"{self.user}"

def create_profile(instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        OTP.objects.create(user=instance)

post_save.connect(create_profile, sender=User)