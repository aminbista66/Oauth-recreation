from pyexpat import model
from django import forms
from .models import Client, ClientScope

class ClientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = (
            'client_id',
            'client_secret',
            'application_type',
            'callback_uri',
        )

class AddScopeForm(forms.ModelForm):
    class Meta:
        model = ClientScope
        fields = (
            'scope',
        )