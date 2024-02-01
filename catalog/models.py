from datetime import datetime

from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория')
    description = models.TextField(**NULLABLE, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=250, verbose_name='Наименование', **NULLABLE)
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    preview = models.ImageField(upload_to='catalog/', verbose_name='Изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', **NULLABLE)
    price = models.IntegerField(verbose_name='Цена за единицу', **NULLABLE)
    created_at = models.DateField(verbose_name='Дата создания', auto_now_add=True, **NULLABLE)
    last_changed_at = models.DateField(verbose_name='Последнее изменение', auto_now=True, **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Владелец', **NULLABLE)
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')

    def __str__(self):
        return f'{self.name} ({self.category})'

    @property
    def active_version(self):
        return Version.objects.filter(is_active=True, product_id=self.pk).first()

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('category', 'name',)
        permissions = [
            ('set_is_published','Изменить статус продукта'),
        ]


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    number = models.IntegerField(default=1, verbose_name='Номер')
    name = models.CharField(max_length=100, default='Создана', verbose_name='Название')
    is_active = models.BooleanField(default=True, verbose_name='Активная')

    def __str__(self):
        return f'{self.name} {self.number}'

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
