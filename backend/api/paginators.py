from rest_framework.pagination import PageNumberPagination

from recipes.constants import PAGINATORS_PAGES


class CustomPadgination(PageNumberPagination):
    """Кастомный паджинатор."""

    page_size = PAGINATORS_PAGES
    page_size_query_param = 'limit'
