from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ListSerializer

from users.models import Follow, User
from users.serializers import UserSerializer, FollowSerializer #, SubscribeSerializer


class SubscribeViewSet(UserViewSet):
    """Реализовывает подписки пользователя."""

    @action(
        detail=True,
        methods=['GET', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        """Подписка на автора."""

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

    #    @action(
    #    detail=True,
    #    methods=['POST'],
    #)
    #def subscribe(self, request, id):
    #    """Подписка на автора."""
#
    #    user = request.user
    #    author = get_object_or_404(User, id=id)
#
    #    if user == author:
    #        return Response({
    #            'errors': 'Подписка на себя запрещена конвенцией о нарциссизме'
    #        }, status=status.HTTP_400_BAD_REQUEST)
#
    #    if Follow.objects.filter(user=user, author=author).exists():
    #        return Response({
    #            'errors': f'Вы уже подписаны на {author}.'
    #        }, status=status.HTTP_400_BAD_REQUEST)
#
    #    follow = Follow.objects.create(user=user, author=author)
    #    serializer = FollowSerializer(
    #        follow, context={'request': request}
    #    )

    #    return Response(serializer.data, status=status.HTTP_201_CREATED)

    #@action(
    #    detail=True,
    #    methods=['DELETE']
    #)
    #def del_subscribe(self, request, id=None):
    #    """Отписка от автора."""
#
    #    user = request.user
    #    author = get_object_or_404(User, id=id)
    #    follow = Follow.objects.filter(user=user, author=author)
    #    if follow.exists():
    #        follow.delete()
#
    #        return Response(status=status.HTTP_204_NO_CONTENT)
#
    #    return Response({
    #        'errors': 'Вы уже отписались'
    #    }, status=status.HTTP_400_BAD_REQUEST)
#
    #@action(
    #    detail=True,
    #    methods=['GET'],
    #    url_path='subscriptions'
    #)
    #def subscriptions(self, request):
    #    """Вывод подписок."""
#
    #    user = request.user
    #    followed_list = User.objects.filter(following__user=user)
    #    paginator = PageNumberPagination()
    #    paginator.page_size_query_param = 'limit'
    #    authors = paginator.paginate_queryset(
    #        followed_list,
    #        request=request
    #    )
    #    serializer = ListSerializer(
    #        child=SubscribeSerializer(),
    #        context=self.get_serializer_context()
    #    )
    #    return paginator.get_paginated_response(
    #        serializer.to_representation(authors)
    #    )
    #
    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
