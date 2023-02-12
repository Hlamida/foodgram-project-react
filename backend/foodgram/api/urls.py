from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from api.views import IngredientViewSet, RecipesViewSet, TagsViewSet
from users.views import SubscribeViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'users', SubscribeViewSet, basename='users')
router.register('tags', TagsViewSet, basename='tags')
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path(
        'users/subscriptions/',
        SubscribeViewSet.as_view({'get': 'subscriptions', }),
        name='subscriptions',
    ),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
