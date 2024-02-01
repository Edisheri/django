import random
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UUIDField

from catalog.models import NULLABLE


class User(AbstractUser):
    username = None
    # code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    email = models.EmailField(unique=True, verbose_name='Почта')

    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    country = models.CharField(max_length=100, verbose_name='Страна', **NULLABLE)
    # verify_code = models.CharField(max_length=6, default=code, verbose_name='Код вeрификации')
    verify_code = models.UUIDField(default=uuid.uuid4, verbose_name='Код вeрификации', editable=False)
    is_verified = models.BooleanField(default=False, verbose_name='Верификация')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
