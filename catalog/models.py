from django.conf import settings
from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Category(models.Model):
    category = models.CharField(max_length=100, verbose_name="Категория")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("category",)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(
        upload_to="product/", verbose_name="Изображение", **NULLABLE
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Владелец")
    is_published = models.BooleanField(default=False, **NULLABLE, verbose_name="опубликовано")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ("name",)

        permissions = [
            ('set_published', 'Может управлять публикацией продукта'),
            ('change_description', 'Может менять описание продукта'),
            ('change_category', 'Может менять категорию продукта')
        ]

    def has_change_permission(self, owner):
        return self.owner == owner


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    version_num = models.IntegerField(verbose_name="номер версии")
    version_name = models.CharField(max_length=150, verbose_name="название версии")
    version_sign = models.BooleanField(**NULLABLE, verbose_name="признак версии")

    def __str__(self):
        return f"{self.version_name} {self.product}"

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
        ordering = ("product", "version_num")
