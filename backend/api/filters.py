from rest_framework.filters import SearchFilter


class IngredientsFilter(SearchFilter):
    """Фильтр ингредиентов."""

    search_param = 'name'
