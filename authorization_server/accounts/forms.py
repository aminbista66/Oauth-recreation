from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import OTP, User
from .validators import validate_phone

class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(validators=[validate_phone])
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'phone',
            'password1',
            'password2',
        )

class OTPForm(forms.ModelForm):
    class Meta:
        model = OTP
        fields = (
            'code',
        )