from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.filters import IngredientsFilter
from api.paginators import CustomPadgination
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (FollowSerializer, RecipeGetSerializer,
                             IngredientSerializer,
                             RecipeListSerializer, TagSerializer)
from api.utils import add_or_delete, get_shopping_list
from recipes.models import Cart, Favorite, Ingredient, Recipe, Tag
from users.models import Follow, User
from users.serializers import UserSerializer


class SubscribeViewSet(UserViewSet):
    """Реализовывает подписки пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPadgination
    permission_classes = (IsAuthenticated,)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        url_path='subscribe',
        permission_classes=(IsAuthenticated,),
    )
    def subscribe(self, request, id):
        """Подписка на автора, удаление подписки."""

        user = request.user
        author = get_object_or_404(User, id=id)

        if request.method == 'POST':
            follow = Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(
                follow.author, context={'request': request}
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            Follow.objects.filter(
                user=user, author=author
            ).delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({
            'errors': 'Вы уже отписались'
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        url_path='subscriptions',
        permission_classes=(IsAuthenticated,),
    )
    def subscriptions(self, request):
        """Вывод списка подписок пользователя."""

        user = request.user
        following_list = User.objects.filter(following__user=user)
        pages = self.paginate_queryset(following_list)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )

        return self.get_paginated_response(serializer.data)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Работа с тегами."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Работа с ингредиентами."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (IngredientsFilter,)
    search_fields = ('^name',)


class RecipesViewSet(viewsets.ModelViewSet):
    """Работа с рецептами."""

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CustomPadgination

    def get_serializer_class(self):
        """Выбор сериализатора."""

        if self.request.method == 'GET':
            return RecipeGetSerializer

        return RecipeListSerializer

    def get_queryset(self):
        """Фильтрация содержимого выводимого кверисета."""

        query_tags = self.request.query_params.getlist('tags')
        query_author = self.request.query_params.get('author')

        if 'author' in self.request.query_params:
            return Recipe.objects.filter(
                author=query_author, tags__slug__in=query_tags
            ).distinct()

        if 'is_favorited' in self.request.query_params:
            return Recipe.objects.filter(
                favorite__user=self.request.user, tags__slug__in=query_tags
            ).distinct()

        if 'is_in_shopping_cart' in self.request.query_params:
            return Recipe.objects.filter(cart__user=self.request.user)

        if query_tags:
            return Recipe.objects.filter(tags__slug__in=query_tags).distinct()

        return Recipe.objects.all()

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        url_path='favorite',
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request, pk=None):
        """Добавляет рецепт в избранное или удаляет его."""

        return add_or_delete(request, Favorite, pk)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        url_path='shopping_cart',
        permission_classes=(IsAuthenticated,),
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
