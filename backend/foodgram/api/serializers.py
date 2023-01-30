import re
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.core.exceptions import ValidationError
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from djoser.serializers import TokenCreateSerializer, SetPasswordSerializer
from users.models import User
from recipes.models import Ingredient, Recipe, Tag


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    is_subscribed = serializers.BooleanField(default=False, read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed',
        )


class UserCreateSerializer(BaseUserRegistrationSerializer):
    """Сериализатор для создания пользователя."""

    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password',
        )


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


class RecipeSerialzer(serializers.ModelSerializer):
    """Сериализатор рецептов."""

    #author = serializers.SlugRelatedField(
    #    slug_field='username',
    #    read_only=True,
    #)

    #is_favorited = serializers.BooleanField(default=False, read_only=True)
#
    #is_in_shopping_cart = serializers.BooleanField(
    #    default=False,
    #    read_only=True,
    #)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',
        )
