from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from enumchoicefield import ChoiceEnum, EnumChoiceField

from recipes.constants import (
    MIN_COOKING_TIME,
    MIN_QUANTITY,
)
from users.models import User
from users.validators import validate_hex


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

    def __str__(self):
        return self.name


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
        validators=(validate_hex,),
        blank=False,
        null=False,
        verbose_name='Цвет в HEX',
    )

    slug = models.SlugField(
        max_length=200,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Уникальный слаг',
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""

    tags = models.ManyToManyField(
        Tag,
        through='RecipeTags',
        verbose_name='Тег',
        related_name='recipe',
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        related_name='recipe',
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredients',
        verbose_name='Список ингредиентов',
        related_name='recipe',
    )

    name = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Название рецепта',
    )

    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        blank=True,
        default=None,
        verbose_name='Картинка рецепта',
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

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    """Модель для связи рецептов с ингредиентами."""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
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
        default=MIN_QUANTITY,
        verbose_name='Количество',
    )


class RecipeTags(models.Model):
    """Модель для связи рецептов с тегами."""

    tags = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class Favorite(models.Model):
    """Определяет модель для избранных рецептов ."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Кто добавляет в избранное',
        related_name='favorite',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Избранный рецепт',
        related_name='favorite',
    )
    UniqueConstraint(
        fields=['user', 'recipe'], name='unique_favorites'
    )

    def __str__(self):
        return self.name


class Cart(models.Model):
    """Определяет модель корзины покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='cart',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='cart',
    )
    UniqueConstraint(
        fields=['user', 'recipe'], name='unique_cart'
    )

    def __str__(self):
        return self.name
