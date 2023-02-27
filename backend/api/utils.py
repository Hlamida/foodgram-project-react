from api.serializers import FavoritedSerializer
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from recipes.models import Recipe, RecipeIngredients
from rest_framework import status
from rest_framework.response import Response


def get_shopping_list(request):
    """Создаёт список покупок."""

    shopping_list = RecipeIngredients.objects.filter(
            recipe__cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(sum_amount=Sum('amount'))
    content = (
        [f'{item["ingredient__name"]}'
         f' ({item["ingredient__measurement_unit"]}) '
         f'- {item["sum_amount"]}\n'
         for item in shopping_list]
    )
    filename = 'shopping_list.txt'
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = (
        'attachment; filename={0}'.format(filename)
    )

    return response


def add_or_delete(request, model, obj_id):
    """Добавляет или удаляет данные."""

    if request.method == 'DELETE':
        obj = model.objects.filter(
            user=request.user,
            recipe__id=obj_id,
        )
        if obj.exists():
            obj.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {'errors': 'Удаление уже произведено'},
            status=status.HTTP_400_BAD_REQUEST)

    if model.objects.filter(
        user=request.user,
        recipe__id=obj_id,
    ).exists():

        return Response(
            status=status.HTTP_400_BAD_REQUEST)

    recipe = get_object_or_404(
        Recipe,
        id=obj_id,
    )
    model.objects.create(
        user=request.user,
        recipe=recipe,
    )
    serializer = FavoritedSerializer(recipe)

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED,
    )
