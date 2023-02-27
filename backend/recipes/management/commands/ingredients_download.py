import json
import os

from django.conf import settings
from django.core.management import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    """Загружает список ингредиентов из файла."""

    def handle(self, *args, **options):

        print('Начинается импорт ингредиентов')
        try:
            path = os.path.join(
                settings.BASE_DIR, '../data/', 'ingredients.json',
            )
            ingredients = json.load(open(path, 'r', encoding='utf8'))
            Ingredient.objects.bulk_create(
                [Ingredient(**ingredient) for ingredient in ingredients],
                ignore_conflicts=True,
            )
            print('Загрузка ингредиентов завершена')

        except FileNotFoundError:
            print('Файл с ингредиентами не найден')
