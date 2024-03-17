from django.contrib import admin

from catalog.models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category", "image",)
    list_filter = ("category",)
    search_fields = ("name", "description",)
