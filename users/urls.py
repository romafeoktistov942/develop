from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import PasswordResetView, UserCreateView, email_verification


app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("verification/<str:token>/", email_verification, name="verification"),
    path("password_reset/", PasswordResetView.as_view(), name="password_reset"),
]
