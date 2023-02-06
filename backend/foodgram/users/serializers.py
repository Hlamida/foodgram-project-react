from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer

from recipes.models import Recipe
from users.models import Follow, User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        """Определяет, подписан ли пользователь на авторов."""

        return Follow.objects.filter(
            author=obj, user=self.context.get('request').user
        ).exists()


class UserCreateSerializer(BaseUserRegistrationSerializer):
    """Сериализатор для создания пользователя."""

    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password',
        )


class GetRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов для подписок."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор подписок."""

    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        """Определение поля is_subscribed."""

        return Follow.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    def get_recipes(self, obj):
        """Определение поля recipes."""

        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]

        return GetRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        """Определение поля recipes_count."""

        return Recipe.objects.filter(author=obj.author).count()
