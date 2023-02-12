from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from api.serializers import FollowRecipeSerializer
from recipes.models import Cart, Recipe


def get_shopping_list(request):
    shopping_cart = Cart.objects.filter(user=request.user).all()
    shopping_list = {}
    for item in shopping_cart:
        for recipe_ingredient in item.recipe.recipe_ingredients.all():
            name = recipe_ingredient.ingredient.name
            measuring_unit = recipe_ingredient.ingredient.measurement_unit
            amount = recipe_ingredient.amount
            if name not in shopping_list:
                shopping_list[name] = {
                    'name': name,
                    'measurement_unit': measuring_unit,
                    'amount': amount
                }
            else:
                shopping_list[name]['amount'] += amount
    content = (
        [f'{item["name"]} ({item["measurement_unit"]}) '
         f'- {item["amount"]}\n'
         for item in shopping_list.values()]
    )
    filename = 'shopping_list.txt'
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = (
        'attachment; filename={0}'.format(filename)
    )
    return response


def add_or_delete(request, model, obj_id):
    user = request.user
    if request.method == 'DELETE':
        obj = model.objects.filter(
            user=user,
            recipe__id=obj_id
        )
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            status=status.HTTP_400_BAD_REQUEST)
    if model.objects.filter(
        user=user,
        recipe__id=obj_id
    ).exists():
        return Response(
            status=status.HTTP_400_BAD_REQUEST)
    recipe = get_object_or_404(
        Recipe,
        id=obj_id
    )
    model.objects.create(
        user=user,
        recipe=recipe
    )
    serializer = FollowRecipeSerializer(recipe)
    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )
