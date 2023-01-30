from django.core.validators import MinValueValidator
from django.db import models
from enumchoicefield import ChoiceEnum, EnumChoiceField

from recipes.constants import MIN_COOKING_TIME, MIN_QUANTITY
from users.models import User


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Название',
    )

    amount = models.IntegerField(
        validators=(
            MinValueValidator(
                MIN_QUANTITY,
                message=f'''
                Количество не может быть меньше {MIN_QUANTITY}
                ''',
            ),
        ),
        blank=False,
        null=False,
        verbose_name='Количество',
    )

    measurement_unit = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        default='гр.',
        verbose_name='Единицы измерения',
    )


class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Название',
    )

    color = models.CharField(
        max_length=7,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Цвет в HEX',
    )

    slug = models.SlugField(
        max_length=200,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Уникальный слаг',
    )


class Includes(ChoiceEnum):
    """Модель для включения в списки."""

    included = 'Включён'
    not_included = 'Не включён'


class Recipe(models.Model):
    """Модель рецептов."""

    tags = models.ManyToManyField( #Array of objects (Tag)
        Tag,
        through='RecipeTags',
        verbose_name='Список тегов',
        related_name='tags',
    )

    author = models.ForeignKey(
        User,  # Дописать, что это автор рецепта
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        related_name='author',
    )

    is_favorited = EnumChoiceField(Includes, default=Includes.not_included)
    is_in_shopping_cart = EnumChoiceField(
        Includes, default=Includes.not_included
    )

    ingredients = models.ManyToManyField( # Array of objects (IngredientInRecipe)
        Ingredient,
        through='RecipeIngredients',
        verbose_name='Список ингредиентов',
        related_name='ingredients',
    )

    name = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        verbose_name='Название рецепта',
    )

    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None
    )

    text = models.TextField(
        blank=False,
        null=False,
        verbose_name='Описание рецепта',
        default='Собираюсь с мыслями..'
    )

    cooking_time = models.IntegerField(
        validators=(
            MinValueValidator(
                MIN_COOKING_TIME,
                message=f'''
                Время приготовления не может быть меньше {MIN_COOKING_TIME}
                ''',
            ),
        ),
        blank=False,
        null=False,
        verbose_name='Время приготовления (в минутах)',
    )


class RecipeIngredients(models.Model):
    """Модель для связи рецептов с ингредиентами."""

    ingredients = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class RecipeTags(models.Model):
    """Модель для связи рецептов с тегами."""

    tags = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
