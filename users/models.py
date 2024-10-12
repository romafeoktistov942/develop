from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="email")

    phone = models.CharField(max_length=35, blank=True, null=True, verbose_name="Телефон", help_text="Ведите номер телефона")
    cantry = models.CharField(max_length=35, blank=True, null=True, verbose_name="Страна", help_text="Ведите страну")
    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True, verbose_name="Аватар", help_text="Загрузите своий аватар")
    token = models.CharField(max_length=255, blank=True, null=True, unique=True, verbose_name="Токен")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Meta:
    verbose_name = "Пользователь"
    verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
