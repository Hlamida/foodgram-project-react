from django.core.mail import EmailMessage
#from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

#from api.filters import TitlesFilter
#from api.utils import CategoryGenreMixin
from api.filters import RecipesFilter
from api.permissions import (IsAdminOnly, IsAdminOrReadOnly,
                             IsAuthorOrReadOnly,
)
from api.serializers import ( 
    IngredientSerializer, TagSerializer, RecipeCreateSerialzer, RecipeListSerialzer,
    FollowRecipeSerializer, CartSerializer,
)
from users.serializers import UserSerializer

from recipes.models import Ingredient, Recipe, Tag, Favorite, Cart
from users.models import User
from api.utils import get_shopping_list


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
    serializer_class = RecipeListSerialzer
    permission_classes = (IsAuthorOrReadOnly,)
    filterset_class = RecipesFilter

    #def get_serializer_class(self):
    #    """Выбирает сериализатор в зависимости от запроса."""
#
    #    if self.action in ['create']:
    #        return RecipeCreateSerialzer
#
    #    return RecipeListSerialzer

    def perform_create(self, serializer):
        """Передает сериализатору автора рецепта."""

        serializer.save(
            author=self.request.user,
        )

    @action(
        detail=True,
        methods=['GET', 'DELETE'],
        permission_classes=[IsAuthenticatedOrReadOnly],
        url_path='favorite'
    )
    def favorite(self, request, pk):
        """Добавление рецептов в избранное."""

        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'GET':
            favorite_recipe, created = Favorite.objects.get_or_create(
                user=user,
                recipe=recipe,
            )
            if created is True:
                serializer = FollowRecipeSerializer()

                return Response(
                    serializer.to_representation(instance=favorite_recipe),
                    status=status.HTTP_201_CREATED,
                )
        if request.method == 'DELETE':
            Favorite.objects.filter(
                user=user,
                recipe=recipe,
            ).delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['GET', 'DELETE'],
        permission_classes=[IsAuthenticatedOrReadOnly]
    )
    def shopping_cart(self, request, pk):
        """Добавление рецептов в корзину."""

        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'GET':
            recipe, created = Cart.objects.get_or_create(
                user=user,
                recipe=recipe,
            )
            if created is True:
                serializer = CartSerializer()

                return Response(
                    serializer.to_representation(instance=recipe),
                    status=status.HTTP_201_CREATED,
                )

            return Response(
                {'errors': 'Рецепт уже добавлен'},
                status=status.HTTP_201_CREATED,
            )

        if request.method == 'DELETE':
            Cart.objects.filter(
                user=user,
                recipe=recipe,
            ).delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)

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
