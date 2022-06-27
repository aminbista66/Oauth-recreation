from django.contrib import admin

from .models import User, Profile, OTP

class UserDisplay(admin.ModelAdmin):
    list_display = ("email", "username", "phone",)

class profileDisplay(admin.ModelAdmin):
    list_display = ("user", "is_verified",)

class OTPDisplay(admin.ModelAdmin):
    list_display = ("user", "code",)

admin.site.register(User, UserDisplay)
admin.site.register(Profile, profileDisplay)
admin.site.register(OTP, OTPDisplay)