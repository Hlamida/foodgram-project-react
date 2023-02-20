from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from api.views import (
    IngredientViewSet, RecipesViewSet,
    SubscribeViewSet, TagsViewSet,
)

app_name = 'api'

router = DefaultRouter()
router.register('users', SubscribeViewSet, basename='users')
router.register('tags', TagsViewSet, basename='tags')
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
