from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="почта")
    phone = models.CharField(max_length=35, **NULLABLE, verbose_name="телефон")
    avatar = models.ImageField(upload_to="users/", **NULLABLE, verbose_name="аватар")
    country = models.CharField(max_length=150, verbose_name="страна")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
