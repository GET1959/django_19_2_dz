from django.db import models


NULLABLE = {'blank': True, 'null': True}

class Category(models.Model):
    category = models.CharField(max_length=100, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('category',)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='product/', verbose_name='Изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('name',)
