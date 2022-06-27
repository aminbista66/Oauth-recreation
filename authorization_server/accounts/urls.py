from django.urls import path, reverse_lazy
from accounts.views import (
    SignUpView,
    CustomLoginView,
    verify_token,
    OTPView,
    TempHome,
    CustomPasswordResetView,
)
from django.contrib.auth.views import (
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

app_name = "accounts"

urlpatterns = [
    path("sign-up/", SignUpView.as_view(), name="sing_up"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("otp-auth/", OTPView.as_view(), name="otp_auth"),
    path("verify-token/<slug:token>/", verify_token, name="verify_token"),
    path("password-reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url = reverse_lazy('accounts:password_reset_complete')
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("home/", TempHome.as_view(), name="home"),
]
