from django.contrib import admin
from .models import Scope, Client, ClientScope, AuthCode

class ClientDisplay(admin.ModelAdmin):
    list_display = ('user', 'application_type', 'client_id', 'callback_uri', )

class ScopeDisplay(admin.ModelAdmin):
    list_display = ('label',)

class ClientScopeDisplay(admin.ModelAdmin):
    list_display = ('client', 'scope')

class AuthCodeDisplay(admin.ModelAdmin):
    list_display = ('user', 'code', 'issued_at',)

admin.site.register(Scope, ScopeDisplay)
admin.site.register(Client, ClientDisplay)
admin.site.register(ClientScope, ClientScopeDisplay)
admin.site.register(AuthCode, AuthCodeDisplay)