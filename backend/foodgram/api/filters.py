from django_filters import rest_framework as filters

from recipes.models import Recipe


class RecipesFilter(filters.FilterSet):
    """Класс для фильтрации рецептов."""

    tag = filters.CharFilter(
        field_name='tag__slug',
        lookup_expr='contains',
    )
    author = filters.CharFilter(
        field_name='author__username',
        lookup_expr='icontains',
    )
    is_favorited = filters.NumberFilter(
        field_name='is_favorited',
        lookup_expr='contains',
    )
    is_in_shopping_cart = filters.NumberFilter(
        field_name='is_in_shopping_cart',
        lookup_expr='contains',
    )

    #class Meta:
    #    model = Recipe
    #    fields = {
    #        'first_name': ['startswith'],
    #        'last_name': ['startswith'],
    #    }
