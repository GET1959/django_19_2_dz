# Generated by Django 5.0.3 on 2024-04-08 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_alter_version_version_sign'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='current_version',
            field=models.IntegerField(default=1, verbose_name='Действующая версия'),
        ),
    ]
