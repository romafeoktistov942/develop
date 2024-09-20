from django.db import models


class Blog(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.CharField(max_length=255, unique=True, db_index=True, null=True, blank=True, verbose_name="slug")
    body = models.TextField(max_length=250, verbose_name='Описание', blank=True, null=True)
    image = models.ImageField(upload_to='products/photo', verbose_name='Изображение', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Признак публикации')
    views_counter = models.IntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
