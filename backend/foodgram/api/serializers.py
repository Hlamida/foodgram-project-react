import re
import traceback

from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.core.exceptions import ValidationError
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from djoser.serializers import TokenCreateSerializer, SetPasswordSerializer
from drf_extra_fields.fields import Base64ImageField

from users.models import Follow, User
from recipes.models import Cart, Favorite, RecipeTags, Ingredient, Recipe, Tag, RecipeIngredients


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""

    class Meta:
        model = Tag
        fields = (
            'id', 'name', 'color', 'slug',
        )
        lookup_field = 'slug'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    class Meta:
        model = Ingredient
        fields = (
            'id', 'name', 'measurement_unit',
        )


class IngredientsRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов для рецептов."""

    #id = serializers.PrimaryKeyRelatedField(
    #    queryset=Ingredient.objects.all(),
    #    source='ingredient.id'
    #)
    #name = serializers.CharField(
    #    source='ingredient.name',
    #    read_only=True,
    #)
    #measurement_unit = serializers.CharField(
    #    source='ingredient.measurement_unit',
    #    read_only=True,
    #)

    #class Meta:
    #    model = RecipeIngredients
    #    fields = ('id', 'name', 'measurement_unit', 'amount')
    id = serializers.ReadOnlyField(
        source='ingredient.id',
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name',
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор автора рецепта."""

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',)


class RecipeListSerialzer(serializers.ModelSerializer):
    """Сериализатор рецептов."""

    tags = TagSerializer(
        read_only=True,
        many=True,
    )
    author = AuthorSerializer(
        read_only=True,
    )
    ingredients = IngredientsRecipeSerializer(
        source='recipe_ingredients',
        many=True,
    )
    image = Base64ImageField(
        max_length=None,
        use_url=True,
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',
        )

    def get_is_favorited(self, obj):
        """Определяет, в избранном ли рецепт."""

        if not self.context.get('request').user.pk:
            return None

        return Favorite.objects.filter(
            recipe=obj.id,
            user=self.context.get('request').user
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        """Определяет, есть ли рецепт в списке покупок."""

        if not self.context.get('request').user.pk:
            return None

        return Cart.objects.filter(
            recipe=obj.id,
            user=self.context.get('request').user
        ).exists()

    #def create(self, validated_data):
    #    context = self.context['request']
    #    ingredients = validated_data.pop('recipe_ingredients')
    #    try:
    #        recipe = Recipe.objects.create(
    #            **validated_data,
    #            author=self.context.get('request').user
    #        )
    #    except IntegrityError as err:
    #        pass
    #    tags_set = context.data['tags']
    #    for tag in tags_set:
    #        RecipeTags.objects.create(
    #            recipe=recipe,
    #            tag=Tag.objects.get(id=tag)
    #        )
    #    ingredients_set = context.data['ingredients']
    #    for ingredient in ingredients_set:
    #        ingredient_model = Ingredient.objects.get(id=ingredient['id'])
    #        RecipeIngredients.objects.create(
    #            recipe=recipe,
    #            ingredient=ingredient_model,
    #            amount=ingredient['amount'],
    #        )
    #    return recipe

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            RecipeIngredients.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )

    def create(self, validated_data):
        image = validated_data.pop('image')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(image=image, **validated_data)
        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)
        self.create_ingredients(ingredients_data, recipe)
        return recipe

    #def to_representation(self, instance):
    #    response = super(RecipeListSerialzer, self).to_representation(instance)
    #    if instance.image:
    #        response['image'] = instance.image.url
    #    return response


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


class FollowRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта для подписок."""

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор подписок."""

    id = serializers.ReadOnlyField(
        source='author.id',
    )
    email = serializers.ReadOnlyField(
        source='author.email',
    )
    username = serializers.ReadOnlyField(
        source='author.username',
    )
    first_name = serializers.ReadOnlyField(
        source='author.first_name',
    )
    last_name = serializers.ReadOnlyField(
        source='author.last_name',
    )
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        return FollowRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()


class CartSerializer(serializers.ModelSerializer):
    """Сериализатор корзины покупок."""

    id = serializers.ReadOnlyField(
        source='recipe.id',
    )
    cooking_time = serializers.ReadOnlyField(
        source='recipe.cooking_time',
    )
    image = serializers.ReadOnlyField(
        source='recipe.image',
    )
    name = serializers.ReadOnlyField(
        source='recipe.name',
    )

    class Meta:
        model = Cart
        fields = ('id', 'cooking_time', 'name', 'image')
