from django.contrib import admin

from catalog.models import Product, Category, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "category",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "category",
        "image",
    )
    list_filter = ("category",)
    search_fields = (
        "name",
        "description",
    )


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "version_num",
        "version_name",
        "version_sign",
    )
