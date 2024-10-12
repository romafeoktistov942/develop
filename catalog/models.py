from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование")
    description = models.TextField(
        max_length=255,
        verbose_name="Описание",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование")
    description = models.TextField(
        max_length=255,
        verbose_name="Описание",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="products/images",
        verbose_name="Изображение",
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        blank=True,
        null=True,
        related_name="products",
    )
    # manufactured_at = models.DateTimeField(null=True, blank=True)
    price = models.FloatField(verbose_name="Цена за покупку")
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец", null=True, blank=True)
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего изменения",
        blank=True,
        null=True,
    )
    views_counter = models.PositiveBigIntegerField(
        verbose_name="Количество просмотров", default=0
    )
    @property
    def active_versions(self):
        return self.versions.filter(is_active=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class Version(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="versions",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Продукт",
    )

    version_number = models.PositiveIntegerField(verbose_name="Номер версии")

    version_name = models.CharField(max_length=150, verbose_name="Название версии")

    is_active = models.BooleanField(verbose_name="Признак текущей версии")
   
    def save(self, *args, **kwargs):
        print("Сохраняем версию...")
        if not self.product.versions.filter(is_active=True).exists():
            print("Нет активных версий, устанавливаем в True...")
            self.is_active = True
        super().save(*args, **kwargs)
        print("Версия сохранена...")

    @classmethod
    def create(cls, **kwargs):
        print("Создаем новую версию...")
        instance = cls(**kwargs)
        instance.save()
        print("Версия создана...")
        return instance

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"

    def __str__(self):
        return f"{self.product} {self.version_number} {self.version_name} {self.is_active}"
    
    @receiver(post_save, sender=Product)
    def set_default_version(sender, instance, created, **kwargs):
        if created and not instance.versions.exists():
            # Создаем новую версию по умолчанию для продукта
            Version.objects.create(
                product=instance,
                version_number=1,
                version_name='Версия по умолчанию',
                is_active=True
            )
        elif instance.versions.exists() and not instance.versions.filter(is_active=True).exists():
            # Если нет активных версий, устанавливаем последнюю версию как активную
            instance.versions.last().is_active = True
            instance.versions.last().save()