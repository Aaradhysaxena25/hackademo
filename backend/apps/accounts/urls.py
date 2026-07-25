"""URL patterns for the accounts app."""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = "accounts"

urlpatterns = [
    # Authentication
    path("auth/register/", views.RegisterView.as_view(), name="register"),
    path("auth/login/", views.LoginView.as_view(), name="login"),
    path("auth/logout/", views.LogoutView.as_view(), name="logout"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Password
    path("auth/password/change/", views.ChangePasswordView.as_view(), name="password_change"),
    # Profile
    path("profile/", views.ProfileView.as_view(), name="profile"),
]
