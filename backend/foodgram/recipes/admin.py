from django.contrib import admin



from recipes.models import Ingredient, Recipe, Tag


class TagAdmin(admin.ModelAdmin):
    """Определяет структуру вывода информации о тегах."""

    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    search_fields = ('name',)
    #list_filter = ('pub_date',)
    #list_editable = ('group',)
    #empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    """Определяет структуру вывода информации об ингредиентах."""

    list_display = (
        'id',
        'name',
        'amount',
        'measurement_unit',
    )
    search_fields = ('name',)


class RecipeInline(admin.TabularInline):
    model = Recipe


class TagInline(admin.TabularInline):
    model = Tag
    fk_name = 'recipe'


#class RecipeAdmin(admin.ModelAdmin):
#    """Определяет структуру вывода информации о рецептах."""
#
#    inlines = [
#        RecipeInline,
#        TagInline,
#    ]

    #list_display = (
    #    'id',
    #    'author',
    #    'name',
    #    'text',
    #    'cooking_time',
    #)
    #search_fields = ('name',)

admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
#admin.site.register(Recipe, RecipeAdmin)
#admin.site.register(Group)
#admin.site.register(Comment)
