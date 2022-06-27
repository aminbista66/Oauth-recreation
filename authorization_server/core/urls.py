from argparse import Namespace
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("accounts.urls", namespace="accounts")),
    path('c/', include("CAuth.urls", namespace="c_auth")),
]
