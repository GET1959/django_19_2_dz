from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    slug = models.CharField(max_length=150, verbose_name="slug", null=True, blank=True)
    body = models.TextField(verbose_name="Содержимое")
    preview = models.ImageField(upload_to="blog/", null=True, blank=True, verbose_name="Изображение")
    create_date = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=True, verbose_name="опубликовано")
    views_count = models.IntegerField(default=0, verbose_name="просмотры")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "публикации"
