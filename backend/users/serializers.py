from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers

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
