from django_filters.rest_framework import FilterSet, filters
from django_filters.widgets import BooleanWidget
from recipes.models import Recipe
from rest_framework.filters import SearchFilter
from users.models import User


class RecipesFilter(FilterSet):
    """Класс для фильтрации рецептов."""

    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_in_shopping_cart = filters.BooleanFilter(
        widget=BooleanWidget(), label='В корзине.'
    )
    is_favorited = filters.BooleanFilter(
        widget=BooleanWidget(), label='В избранных.'
    )
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug',
                                           label='Ссылка')

    class Meta:
        model = Recipe
        fields = ['is_favorited', 'is_in_shopping_cart', 'author', 'tags']


class IngredientsFilter(SearchFilter):
    """Фильтр ингредиентов."""

    search_param = 'name'
