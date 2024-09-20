from django.db import models


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

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего изменения",
        blank=True,
        null=True,
    )
    views_counter = models.PositiveBigIntegerField(
        verbose_name="Количество просмотров", default=0
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class Version(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="product",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Продукт",
    )

    number = models.PositiveIntegerField(verbose_name="Номер версии")

    name = models.CharField(max_length=150, verbose_name="Название версии")

    is_active = models.BooleanField(verbose_name="Признак текущей версии")

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"

    def __str__(self):
        return f"{self.number} - {self.name}"
