from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "CAuth"

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name="c_login"),
    path('otp-auth/', views.OTPView.as_view(), name="c_otp_auth"),
    path('auth-grant-confirmation/', views.GetAuthGrantConfirmation.as_view(), name="auth_grant_confirmation"),
    path('auth-grant/', views.GetAuthGrant.as_view(), name="auth_grant"),
    
    path('token-refresh/', TokenRefreshView.as_view(), name="token_refresh")
]