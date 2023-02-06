import re
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.core.exceptions import ValidationError
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from djoser.serializers import TokenCreateSerializer, SetPasswordSerializer
from users.models import Follow, User
from recipes.models import Favorite, Ingredient, Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""

    class Meta:
        model = Tag
        fields = (
            'id', 'name', 'color', 'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    class Meta:
        model = Ingredient
        fields = (
            'id', 'name', 'measurement_unit',
        )


class RecipeListSerialzer(serializers.ModelSerializer):
    """Сериализатор рецептов."""

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        slug_field='slug',
        many=True,
    )
#
    #is_in_shopping_cart = serializers.BooleanField(
    #    default=False,
    #    read_only=True,
    #)

    # is_favorited = serializers.BooleanField(default=False, read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',
        )
        read_only_fields = ['author']

    def get_is_favorited(self, obj):
        """Определяет, в избранном ли рецепт."""

        if not self.context["request"].user.pk:
            return None

        if Favorite.objects.filter(
            user=self.context['request'].user
        ).exists():
            return 1

        return 0

    def get_is_in_shopping_cart(self, obj):
        """Определяет, есть ли рецепт в списке покупок."""

        if not self.context["request"].user.pk:
            return None

        if Favorite.objects.filter(
            user=self.context['request'].user
        ).exists():
            return 1

        return 0


class RecipeCreateSerialzer(serializers.ModelSerializer):
    """Сериализатор рецептов."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'ingredients', 'tags', 'image', 'author',
            'name', 'text', 'cooking_time',
        )
