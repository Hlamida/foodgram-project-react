from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import RecipesFilter
from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from api.serializers import (IngredientSerializer, RecipeGetSerialzer,
                             RecipeListSerializer, TagSerializer)
from api.utils import add_or_delete, get_shopping_list
from recipes.models import Cart, Favorite, Ingredient, Recipe, Tag


class TagsViewSet(viewsets.ModelViewSet):
    """Работа с тегами."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(viewsets.ModelViewSet):
    """Работа с ингредиентами."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)


class RecipesViewSet(viewsets.ModelViewSet):
    """Работа с рецептами."""

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    filterset_class = RecipesFilter

    def get_serializer_class(self):
        """Выбор сериализатора."""

        if self.request.method == 'GET':
            return RecipeGetSerialzer

        return RecipeListSerializer

    def perform_create(self, serializer):
        """Передает сериализатору автора рецепта."""

        serializer.save(
            author=self.request.user,
        )

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        url_path='favorite',
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        """Добавляет рецепт в избранное или удаляет его."""

        return add_or_delete(request, Favorite, pk)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        url_path='shopping_cart',
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk=None):
        """Добавляет рецепт в корзину или удаляет его."""
        return add_or_delete(request, Cart, pk)

    @action(
        detail=False,
        methods=['GET'],
        url_path='download_shopping_cart',
    )
    def download_shopping_cart(self, request):
        """Выгружает список покупок."""

        if get_shopping_list(request):
            return get_shopping_list(request)

        return Response(status=status.HTTP_400_BAD_REQUEST)
