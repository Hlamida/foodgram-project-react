from django.contrib import admin
from recipes.models import (Cart, Favorite, Ingredient, Recipe,
                            RecipeIngredients, RecipeTags, Tag)


class IngredientsInline(admin.TabularInline):
    """Включённая структура ингредиентов в рецепте."""

    model = RecipeIngredients


class TagsInline(admin.TabularInline):
    """Включённая структура тегов в рецепте."""

    model = RecipeTags


class RecipeAdmin(admin.ModelAdmin):
    """Определяет структуру вывода информации о рецептах."""

    list_display = (
        'name',
        'author',
        'count_favorites',
    )
    list_filter = (
        'name',
        'author',
        'tags',
    )
    search_fields = (
        'name',
        'author',
        'tags',
    )
    inlines = [
        IngredientsInline,
        TagsInline,
    ]

    def count_favorites(self, obj):
        return obj.favorite.count()


class IngredientAdmin(admin.ModelAdmin):
    """Определяет структуру вывода информации об ингредиентах."""

    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)
    search_fields = ('name',)
    inlines = [IngredientsInline]


class TagAdmin(admin.ModelAdmin):
    """Определяет структуру вывода информации о тегах."""

    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    search_fields = ('name',)


class CartAdmin(admin.ModelAdmin):
    """Определяет структуру вывода информации о корзине."""

    list_display = (
        'user',
        'recipe',
    )
    search_fields = (
        'user',
        'recipe',
    )


class FavoriteAdmin(admin.ModelAdmin):
    """Определяет структуру вывода информации об избранном."""

    list_display = (
        'user',
        'recipe',
    )
    search_fields = (
        'user',
        'recipe',
    )


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
