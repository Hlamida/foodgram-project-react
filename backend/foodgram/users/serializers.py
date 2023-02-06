from rest_framework import serializers, validators
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer

from recipes.models import Recipe
from api.serializers import RecipeListSerialzer
from users.mixins import IsSubscribedMixin
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


#class SubscribeSerializer(serializers.ModelSerializer):
#    """Сериализатор подписок."""
#
#    recipes = serializers.SlugRelatedField(
#        queryset=Recipe.objects.all(),
#        slug_field='name',
#        many=True,
#    )
#    recipes_count = serializers.SerializerMethodField()
#    is_subscribed = serializers.SerializerMethodField()
#
#    class Meta:
#        model = User
#        fields = (
#            'email', 'id', 'username', 'first_name', 'last_name',
#            'is_subscribed', 'recipes', 'recipes_count',
#        )
#
#    def get_recipes_count(self, obj):
#        """Считает количество рецептов у автора."""
#
#        return Recipe.objects.filter(author=obj).count()
#
#    def get_is_subscribed(self, obj):
#        """Определяет, подписан ли пользователь на авторов."""
#
#        return Follow.objects.filter(
#            author=obj, user=self.context.get('request').user
#        ).exists()
#
#    def create(self, validated_data):
#        subscribe = Follow.objects.create(**validated_data)
#        subscribe.save()
#        return subscribe


#class SubscribeSerializer(serializers.ModelSerializer, IsSubscribedMixin):
#    recipes = serializers.SerializerMethodField()
#    recipes_count = serializers.SerializerMethodField('get_recipes_count')
#    username = serializers.CharField(
#        required=True,
#        validators=[validators.UniqueValidator(
#            queryset=User.objects.all()
#        )]
#    )
#
#    class Meta:
#        model = User
#        fields = [
#            'email', 'id', 'username', 'first_name', 'last_name',
#            'recipes', 'recipes_count', 'is_subscribed'
#        ]
#
#    def validate(self, data):
#        author = data['following']
#        user = data['follower']
#        if user == author:
#            raise serializers.ValidationError('You can`t follow for yourself!')
#        if (Follow.objects.filter(author=author, user=user).exists()):
#            raise serializers.ValidationError('You have already subscribed!')
#        return data
#
#    def create(self, validated_data):
#        subscribe = Follow.objects.create(**validated_data)
#        subscribe.save()
#        return subscribe
#
#    def get_recipes_count(self, data):
#        return Recipe.objects.filter(author=data).count()
#
#    def get_recipes(self, data):
#        recipes_limit = self.context.get('request').GET.get('recipes_limit')
#        recipes = (
#            data.recipes.all()[:int(recipes_limit)]
#            if recipes_limit else data.recipes
#        )
#        serializer = serializers.ListSerializer(child=RecipeListSerialzer())
#        return serializer.to_representation(recipes)
#

class CropRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
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
        return Follow.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        return CropRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()
