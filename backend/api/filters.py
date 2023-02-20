from django_filters import rest_framework as filters
from rest_framework import filters as fltrs

from recipes.models import Recipe, Tag


class RecipesFilter(filters.FilterSet):
    """Класс для фильтрации рецептов."""

    tags = filters.filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    author = filters.CharFilter(
        field_name='author__username',
        lookup_expr='icontains',
    )
    is_favorited = filters.BooleanFilter(
        field_name='is_favorited',
        method='filter_is_favorited',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart',
        method='filter_is_in_shopping_cart',
    )

    def filter_is_favorited(self, queryset, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(cart__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = {
            'tags',
            'author',
        }


class IngredientsFilter(fltrs.SearchFilter):
    """Фильтр ингредиентов."""

    search_param = 'name'
