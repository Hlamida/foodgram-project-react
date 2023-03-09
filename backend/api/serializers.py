from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (Cart, Favorite, Ingredient, Recipe,
                            RecipeIngredients, Tag)
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

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(
        source='ingredient.name',
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания списка ингредиентов"""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')


#class RecipeListSerializer(serializers.ModelSerializer):
#    """Сериализатор рецептов."""
#
#    tags = TagSerializer(
#        read_only=True,
#        many=True,
#    )
#    author = UserSerializer(
#        read_only=True,
#    )
#    ingredients = RecipeIngredientsSerializer(
#        many=True,
#        allow_empty=False,
#    )
#    image = Base64ImageField(
#        max_length=None,
#        use_url=True,
#    )
#
#    class Meta:
#        model = Recipe
#        fields = (
#            'id', 'tags', 'author', 'ingredients',
#            'name', 'image', 'text', 'cooking_time',
#        )
#
#    def validate(self, obj):
#        """Валидация данных."""
#
#        ingredients = obj.pop('ingredients')
#        if not ingredients:
#            raise serializers.ValidationError(
#                'Отсутствуют ингридиенты')
#        ingredient_list = []
#        for ingredient_item in ingredients:
#            ingredient = get_object_or_404(
#                Ingredient,
#                id=ingredient_item['ingredients.id']
#            )
#            if ingredient in ingredient_list:
#                raise serializers.ValidationError(
#                    'Ингредиент уже добавлен'
#                )
#            ingredient_list.append(ingredient)
#        obj['ingredients'] = ingredients
#
#        return obj
#
#    def add_ingredients(self, ingredients, recipe):
#        """Добавляет ингредиенты."""
#
#        for ingredient in ingredients:
#            if not ingredients:
#                raise serializers.ValidationError(
#                    'Отсутствуют ингридиенты'
#                )
#            amount = ingredient.get('amount')
#            ingredient_instance = get_object_or_404(
#                Ingredient,
#                pk=ingredient['ingredients.id'])
#            RecipeIngredients.objects.create(
#                recipe=recipe,
#                ingredient=ingredient_instance,
#                amount=amount
#            )
#
#    def create(self, validated_data):
#        """Сохраняет рецепт."""
#
#        image = validated_data.pop('image')
#        ingredients_data = validated_data.pop('ingredients')
#        recipe = Recipe.objects.create(image=image, **validated_data)
#        tags_data = self.initial_data.get('tags')
#        recipe.tags.set(tags_data)
#        self.add_ingredients(ingredients_data, recipe)
#
#        return recipe
#
#    def update(self, instance, validated_data):
#        """Изменяет рецепт."""
#
#        ingredients_data = validated_data.pop('ingredients')
#        RecipeIngredients.objects.filter(
#            recipe=instance
#        ).delete()
#        self.add_ingredients(ingredients_data, instance)
#        instance.save()
#
#        return super().update(instance, validated_data)


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/редактирования/удаления рецептов"""
    ingredients = RecipeIngredientsSerializer(many=True)
    tags = TagSerializer(many=True)
    author = UserSerializer(read_only=True)
    image = Base64ImageField()
    is_favorited = serializers.BooleanField(default=False)
    is_in_shopping_cart = serializers.BooleanField(default=False)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )


class RecipeCreateSerializer(RecipeReadSerializer):
    """Сериализатор для работы с рецептами"""
    ingredients = RecipeIngredientCreateSerializer(many=True,
                                                   allow_empty=False)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, allow_empty=False
    )

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time'
        )

    @staticmethod
    def add_ingredients(recipe, ingredients):
        try:
            RecipeIngredients.objects.bulk_create(
                [RecipeIngredients(recipe=recipe,
                                   ingredient=ingredient['id'],
                                   amount=ingredient['amount'])
                 for ingredient in ingredients]
            )
        except KeyError:
            raise serializers.ValidationError(
                'Укажите хотя бы один ингредиент!'
            )

    def validate(self, data):
        ingredients = data.get('ingredients')
        ingredient_id = [ingredient.get('id') for ingredient in ingredients]
        if len(ingredient_id) != len(set(ingredient_id)):
            raise serializers.ValidationError(
                'Ингредиент можно добавить только один раз!'
            )
        return data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            author=self.context['request'].user, **validated_data
        )
        self.add_ingredients(recipe, tags, ingredients)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        RecipeIngredients.objects.filter(recipe=instance).delete()
        self.add_ingredients(instance, ingredients)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        serializer = RecipeReadSerializer(
            instance,
            context={'request': self.context.get('request')}
        )
        return serializer.data


class RecipeGetSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов."""

    tags = TagSerializer(
        read_only=True,
        many=True,
    )
    author = UserSerializer(
        read_only=True,
    )
    ingredients = RecipeIngredientsSerializer(
        #source='recipe_ingredients',
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

        #if Follow.objects.filter(user=user, author=author).exists():
        #    return Response({
        #        'errors': f'Вы уже подписаны на {author}.'
        #    }, status=status.HTTP_400_BAD_REQUEST)

        return user.follower.filter(author=obj).exists()

    def validate(self, data):
        user = self.context.get('request').user
        if user == data['user']:
            raise serializers.ValidationError(
                'Вы не можете подписаться на себя самого'
            )
        if user.follower.filter(author=data['user']).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на него.'
            )

        return data

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
