import random
import secrets
from .forms import PasswordResetForm
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import CreateView
from django.urls import reverse, reverse_lazy
from users.models import User
from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm
from django.contrib.auth.hashers import make_password

from config import settings


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")
    template_name = "users/user_form.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.token = secrets.token_urlsafe(16)
        print("Token:", user.token)
        user.save()
        email = user.email
        token = user.token
        url = f"http://127.0.0.1:8000/users/verification/{token}"
        send_mail(
            subject="Подтверждение регистрации",
            message=f"Для подтверждения регистрации перейдите по ссылке {url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


from django.contrib.auth.views import LoginView


class UserLoginView(LoginView):
    template_name = "users/login.html"

    def get_success_url(self):
        return reverse_lazy("users:profile")


class PasswordResetView(View):
    def get(self, request):
        form = PasswordResetForm()
        return render(request, "users/password_reset.html", {"form": form})

    def post(self, request):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.get(email=email)
            new_password = "".join(
                random.choices(
                    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
                    k=10,
                )
            )
            user.password = make_password(new_password)
            user.save()
            send_mail(
                subject="Восстановление пароля",
                message=f"Ваш новый пароль: {new_password}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
            )
            return redirect(reverse("users:login"))
        return redirect(reverse("users:password_reset"))
