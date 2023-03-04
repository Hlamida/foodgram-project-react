from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Cart, Favorite, Ingredient, Recipe,
                            RecipeIngredients, Tag)
from rest_framework import serializers
from users.models import Follow
from users.serializers import UserSerializer


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

    id = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = (
            'id', 'name', 'measurement_unit',
        )
        read_only_fields = ('name',)


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов для рецептов."""

    id = serializers.IntegerField()
    name = serializers.ReadOnlyField(
        source='ingredient.name',
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeListSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов."""

    tags = TagSerializer(
        read_only=True,
        many=True,
    )
    author = UserSerializer(
        read_only=True,
    )
    ingredients = RecipeIngredientsSerializer(
        source='recipe_ingredients',
        many=True,
    )
    image = Base64ImageField(
        max_length=None,
        use_url=True,
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time',
        )

    def validate(self, obj):
        """Валидация данных."""

        ingredients = obj.pop('recipe_ingredients')
        ingredient_list = []
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(
                Ingredient,
                id=ingredient_item['id']
            )
            if ingredient in ingredient_list:
                raise serializers.ValidationError(
                    'Ингредиент уже добавлен'
                )
            ingredient_list.append(ingredient)
        obj['ingredients'] = ingredients

        return obj

    def add_ingredients(self, ingredients, recipe):
        """Добавляет ингредиенты."""

        for ingredient in ingredients:
            #amount = ingredient.get('amount')
            #ingredient_instance = get_object_or_404(
            #    Ingredient,
            #    pk=ingredient['id'])
            #RecipeIngredients.objects.create(
            #    recipe=recipe,
            #    ingredient=ingredient_instance,
            #    amount=amount
            #)
            RecipeIngredients.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )

    def create(self, validated_data):
        """Сохраняет рецепт."""

        image = validated_data.pop('image')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(image=image, **validated_data)
        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)
        self.add_ingredients(ingredients_data, recipe)

        return recipe

    #def update(self, instance, validated_data):
    #    """Изменяет рецепт."""
#
    #    ingredients_data = validated_data.pop('ingredients')
    #    super().update(instance, validated_data)
    #    RecipeIngredients.objects.filter(
    #        recipe=instance
    #    ).delete()
    #    self.add_ingredients(ingredients_data, instance)
    #    instance.save()
#
    #    return instance

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        RecipeIngredients.objects.filter(recipe=instance).all().delete()
        self.add_ingredients(validated_data.get('ingredients'), instance)
        instance.save()
        return instance


class RecipeGetSerialzer(serializers.ModelSerializer):
    """Сериализатор рецептов."""

    tags = TagSerializer(
        read_only=True,
        many=True,
    )
    author = UserSerializer(
        read_only=True,
    )
    ingredients = RecipeIngredientsSerializer(
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
            'id', 'tags', 'author', 'ingredients', 'name', 'image',
            'text', 'cooking_time', 'is_favorited', 'is_in_shopping_cart',
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


class FollowRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта для подписок."""

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор подписок."""

    email = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        """Определение поля is_subscribed."""

        user = self.context.get('request').user
        return user.follower.filter(author=obj).exists()

    def get_recipes(self, obj):
        """Определение поля recipes."""

        queryset = Recipe.objects.filter(author=obj)
        return FollowRecipeSerializer(
            queryset,
            many=True
        ).data

    def get_recipes_count(self, obj):
        """Определение поля recipes_count."""

        return Recipe.objects.filter(author=obj).count()


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


class FavoritedSerializer(serializers.ModelSerializer):
    """Сериализатор любимых рецептов."""

    id = serializers.CharField(
        read_only=True, source='recipe.id',
    )
    cooking_time = serializers.CharField(
        read_only=True, source='recipe.cooking_time',
    )
    image = serializers.CharField(
        read_only=True, source='recipe.image',
    )
    name = serializers.CharField(
        read_only=True, source='recipe.name',
    )

    class Meta:
        model = Favorite
        fields = ('id', 'cooking_time', 'name', 'image')
