# Generated by Django 5.0.3 on 2024-04-08 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0003_alter_product_created_at_alter_product_updated_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="version",
            name="version_sign",
            field=models.BooleanField(
                blank=True, null=True, verbose_name="признак версии"
            ),
        ),
    ]
