import json
import os
from django.core.management import BaseCommand

from catalog.models import Category, Product


def get_models(file):
    cur_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    path_to_file = os.path.join(cur_dir + "/fixtures/" + file)
    with open(path_to_file, 'rb') as f:
        models_list = json.load(f)
    return models_list


class Command(BaseCommand):

    @staticmethod
    def json_read_categories(file):
        cat_list = [model for model in get_models(file) if model["model"] == "catalog.category"]
        return cat_list

    # Здесь мы получаем данные из фикстурв с категориями

    @staticmethod
    def json_read_products(file):
        prod_list = [model for model in get_models(file) if model["model"] == "catalog.product"]
        return prod_list

    # Здесь мы получаем данные из фикстурв с продуктами

    def handle(self, *args, **options):

        # Удалите все продукты
        # Удалите все категории

        # Создайте списки для хранения объектов
        product_for_create = []
        category_for_create = []

        # Обходим все значения категорий из фиктсуры для получения информации об одном объекте
        for category in Command.json_read_categories('data.json'):
            category_for_create.append(
                Category(category=category["fields"]["category"], description=category["fields"]["description"])
            )

            # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из фиктсуры для получения информации об одном объекте
        for product in Command.json_read_products('data.json'):
            product_for_create.append(
                Product(name=product["fields"]["name"],
                        description=product["fields"]["description"],
                        image=product["fields"]["image"],
                        price=product["fields"]["price"],
                        created_at=product["fields"]["created_at"],
                        updated_at=product["fields"]["updated_at"],
                        # получаем категорию из базы данных для корректной связки объектов
                        category=Category.objects.get(pk=product["fields"]["category"]))
            )

            # Создаем объекты в базе с помощью метода bulk_create()
        Product.objects.bulk_create(product_for_create)