
from django.core.management import BaseCommand
from django.db import connection
from catalog.models import Category, Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        Category.objects.all().delete()
        Product.objects.all().delete()
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE catalog_category_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE catalog_product_id_seq RESTART WITH 1;")

        category_list = [
            {'name': 'Фрукты'},
            {'name': 'Овощи'},
            {'name': 'Напитки'},
            {'name': 'Бакалея'}
        ]
        categories_for_create = []
        for cat in category_list:
            categories_for_create.append(Category(**cat))
        Category.objects.bulk_create(categories_for_create)

        vegetable = Category.objects.get(name="Овощи")
        fruit = Category.objects.get(name="Фрукты")
        drink = Category.objects.get(name="Напитки")
        grocery =Category.objects.get(name="Бакалея")

        product_list = [
            {'name': 'Яблоки', 'description': 'ГренниСмит, 1 кг', 'preview': '', 'category': fruit, 'price': 150},
            {'name': 'Апельсины', 'description': 'Сочные, 1 кг', 'preview': '', 'category': fruit, 'price': 150},
            {'name': 'Помидоры', 'description': 'Фламенко, 1 кг', 'preview': '', 'category': vegetable, 'price': 300},
            {'name': 'Огурцы', 'description': 'Колючие короткоплодные, 1 кг', 'preview': '', 'category': vegetable, 'price': 200},
            {'name': 'Вода', 'description': 'Газированая, 1 шт', 'preview': '', 'category': drink, 'price': 40},
            {'name': 'Сок', 'description': 'Вишневый 1 шт', 'preview': '', 'category': drink, 'price': 150},
            {'name': 'Печенье', 'description': 'Овсяное с изюмом, 1 уп', 'preview': '', 'category': grocery, 'price': 100},
            {'name': 'Зефир', 'description': 'В шоколаде, 1 уп', 'preview': '', 'category': grocery, 'price': 150}
        ]

        products_for_create = []
        for prod in product_list:
            products_for_create.append(Product(**prod))
        Product.objects.bulk_create(products_for_create)