# Generated by Django 5.0.3 on 2024-03-18 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Article",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=150, verbose_name="Заголовок")),
                (
                    "slug",
                    models.CharField(
                        blank=True, max_length=150, null=True, verbose_name="slug"
                    ),
                ),
                ("body", models.TextField(verbose_name="Содержимое")),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="blog/",
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "create_date",
                    models.DateField(auto_now_add=True, verbose_name="Дата создания"),
                ),
                (
                    "is_published",
                    models.BooleanField(default=True, verbose_name="опубликовано"),
                ),
                (
                    "views_count",
                    models.IntegerField(default=0, verbose_name="просмотры"),
                ),
            ],
            options={
                "verbose_name": "публикация",
                "verbose_name_plural": "публикации",
            },
        ),
    ]
