from django.db import models
from django.contrib.auth import get_user_model
import secrets
from datetime import datetime

User = get_user_model()

class Client(models.Model):
    client_id = models.CharField(max_length=1000, default=secrets.token_hex(16))
    client_secret = models.CharField(max_length=1000, default=secrets.token_hex(32))
    application_type = models.CharField(max_length=255, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    callback_uri = models.URLField(null=False, blank=False)

    def __str__(self) -> str:
        return f"{self.client_id} | {self.user}"

class ClientScope(models.Model):
    scope = models.ForeignKey('Scope', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.client.client_id} | {self.scope}"

class Scope(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.label}"

class AuthCode(models.Model):
    code = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user} | {self.code}"