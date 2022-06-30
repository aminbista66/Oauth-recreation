from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from accounts.utils import send_otp
from django.contrib import messages
from accounts.models import User, Profile, OTP
from django.views import generic
from accounts.forms import OTPForm
from .models import AuthCode, Client, ClientScope, Scope
from django.db.models import Q
from .utils import get_auth_code, customClaimToken, IdTokenClaim
import random
import secrets


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

    def dispatch(self, request, *args, **kwargs):
        if len(request.GET) < 3:
            return HttpResponse("Not enough parameters")
        client = Client.objects.filter(client_id=request.GET["client_id"])
        if client.exists():
            client = client.first()
            print(client)
            scope = ClientScope.objects.filter(
                Q(client=client)
            )
            requested_scopes = self.request.GET['scopes'].split(' ')

            ## NEEDS TO BE TESTED - TEST PENDING
            for scope in requested_scopes:
                print(scope)

            if not scope.exists():
                return HttpResponse("provided scope was out of bound.")
        return super().dispatch(request, *args, **kwargs)

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
            return HttpResponseRedirect(
                reverse_lazy("c_auth:c_otp_auth")
                + f"?client_id={self.request.GET['client_id']}&scope={self.request.GET['scope']}&response_type={self.request.GET['response_type']}"
            )
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
                login(self.request, user=user)
                AuthCode.objects.all().delete()
                auth_code = secrets.token_hex(16)
                AuthCode.objects.create(user=user, code=auth_code)
                
                return HttpResponseRedirect(
                    reverse_lazy("c_auth:auth_grant_confirmation")
                    + f"?client_id={self.request.GET['client_id']}&scope={self.request.GET['scope']}&response_type={self.request.GET['response_type']}"
                )
        return HttpResponseRedirect(reverse_lazy("accounts:login"))


class GetAuthGrantConfirmation(generic.TemplateView):
    template_name = "CAuth/confirmation.html"
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        callback_uri = Client.objects.get(client_id=self.request.GET['client_id']).callback_uri
        context.update({
            "client_id": self.request.GET['client_id'],
            "scope": self.request.GET['scope'],
            "response_type": self.request.GET['response_type'],
            "callback_uri": callback_uri
        })
        return context

class GetAuthGrant(generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        client = Client.objects.get(client_id=self.request.GET['client_id'])
        callback_uri = client.callback_uri

        if self.request.GET['response_type'] == "token":
            refresh = customClaimToken.get_token(self.request.user, self.request.GET['scope'])
            return f"{callback_uri}/?refresh_token={str(refresh)}&access_token={str(refresh.access_token)}"
        elif self.request.GET['response_type'] == "id_token":
            refresh = IdTokenClaim.get_token(self.request.user)
            return f"{callback_uri}/?refresh_token={str(refresh)}&access_token={str(refresh.access_token)}"
            
        auth_code = get_auth_code(self.request.user)
        print(auth_code)
        return f"{callback_uri}/?auth_code={auth_code}"