from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, PasswordResetView
from django.views import generic
from .forms import CustomUserCreationForm, OTPForm
from .models import OTP, Profile, User
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from .utils import send_verification_mail, send_otp
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
import random


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            email = form.cleaned_data["email"]
            user_profile = Profile.objects.get(user__email=email)
            status = send_verification_mail(email, user_profile.verify_token)
            if status:
                messages.success(
                    self.request, "A verification link has been sent to your email."
                )
            else:
                messages.error(
                    self.request,
                    "Code could not be sent. Try again later",
                    extra_tags="danger",
                )
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return HttpResponseRedirect(reverse_lazy("accounts:login"))


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

    def form_valid(self, form):
        user = form.get_user()
        user_profile = Profile.objects.get(user__pk=user.pk)
        if not user_profile.is_verified:
            return HttpResponseRedirect(reverse_lazy("accounts:login"))
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        authenticated_user = authenticate(
            request=self.request, username=username, password=password
        )
        if authenticated_user is not None:
            self.request.session["pk"] = authenticated_user.pk
            self.request.session.save()
            user_otp = OTP.objects.get(user__pk=self.request.session["pk"])
            user_otp.code = random.randint(10000, 99999)
            user_otp.save()
            status = send_otp(authenticated_user.phone, user_otp.code)
            if status:
                messages.success(
                    self.request, "A verification code has been sent to your phone."
                )
                print(user_otp.code)
            else:
                messages.error(self.request, "Code could not be sent. Try again later")
            return HttpResponseRedirect(reverse_lazy("accounts:otp_auth"))
        return HttpResponse("user doesnot exists")


class OTPView(generic.CreateView):
    form_class = OTPForm
    template_name = "accounts/otp.html"

    def form_valid(self, form):
        user_otp = OTP.objects.get(user__pk=self.request.session["pk"]).code
        if form.is_valid():
            code = form.cleaned_data["code"]
            if user_otp == code:
                user = User.objects.get(id=self.request.session["pk"])
                login(self.request, user)
                return HttpResponseRedirect(reverse_lazy("accounts:home"))
        return HttpResponseRedirect(reverse_lazy("accounts:login"))


def verify_token(request, token):
    profile = Profile.objects.filter(verify_token=token)
    if profile.exists():
        user_profile = profile.first()
        user_profile.is_verified = True
        user_profile.save()
    return HttpResponseRedirect(reverse_lazy("accounts:login"))


class TempHome(LoginRequiredMixin, generic.TemplateView):
    template_name = "accounts/temp_home.html"


class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name: str = "accounts/password_reset.html"
    email_template_name: str = "accounts/password_reset_email.html"
    success_message: str = "Password reset link has been sent to your email."
    success_url = reverse_lazy("accounts:home")
