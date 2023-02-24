from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from recipes.models import Recipe
from users.models import User


class RecipesFilter(FilterSet):
    """Класс для фильтрации рецептов."""

    tags = filters.AllValuesMultipleFilter(field_name='tags__recipetags__slug')
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = {
            'tags',
            'author',
        }

    def filter_is_favorited(self, queryset, value):

        if value and not self.request.user.is_anonymous:
            return queryset.filter(favorite__user=self.request.user)

        return queryset.filter(favorite__user=self.request.user)

    def filter_is_in_shopping_cart(self, queryset, value):

        if value and not self.request.user.is_anonymous:
            return queryset.filter(cart__user=self.request.user)

        return queryset.filter(cart__user=self.request.user)


class IngredientsFilter(SearchFilter):
    """Фильтр ингредиентов."""

    search_param = 'name'