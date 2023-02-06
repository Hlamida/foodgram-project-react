from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response


from users.models import Follow, User
from users.serializers import FollowSerializer


class SubscribeViewSet(UserViewSet):
    """Реализовывает подписки пользователя."""

    @action(
        detail=True,
        methods=['GET', 'DELETE'],
    )
    def subscribe(self, request, id):
        """Подписка на автора, удаление подписки."""

        following = get_object_or_404(User, id=id)
        follower = request.user

        if request.method == 'GET':
            user = request.user
            author = get_object_or_404(User, id=id)

            if user == author:
                return Response({
                    'errors': 'Подписка на себя запрещена конвенцией о нарциссизме'
                }, status=status.HTTP_400_BAD_REQUEST)

            if Follow.objects.filter(user=user, author=author).exists():
                return Response({
                    'errors': f'Вы уже подписаны на {author}.'
                }, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            Follow.objects.filter(
                user=follower, author=following
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': 'Вы уже отписались'
        }, status=status.HTTP_400_BAD_REQUEST)

    def subscriptions(self, request):
        """Вывод списка подписок пользователя."""

        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
