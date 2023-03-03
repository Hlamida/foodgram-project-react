from django_filters.rest_framework import FilterSet, filters
from recipes.models import Favorite, Recipe, Tag
from rest_framework.filters import SearchFilter


class RecipesFilter(FilterSet):
    """Класс для фильтрации рецептов."""

    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        if not value:
            return queryset
        favorite_recipes_id = Favorite.objects.filter(
            user=self.request.user.id).values_list("recipe__id", flat=True)
        return queryset.filter(id__in=favorite_recipes_id)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if not value:
            return queryset
        shoppingcart_recipes_id = Favorite.objects.filter(
            user=self.request.user.id).values_list("recipe__id", flat=True)
        return queryset.filter(id__in=shoppingcart_recipes_id)


class IngredientsFilter(SearchFilter):
    """Фильтр ингредиентов."""

    search_param = 'name'
