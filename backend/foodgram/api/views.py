from django.core.mail import EmailMessage
#from django.db.models import Avg
#from django.shortcuts import get_object_or_404
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
)
from users.serializers import UserSerializer

from recipes.models import Ingredient, Recipe, Tag
from users.models import User


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
