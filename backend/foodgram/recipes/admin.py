from django.contrib import admin



from recipes.models import Ingredient, Recipe, Tag, RecipeIngredients, RecipeTags


#class RecipeInline(admin.TabularInline):
#    model = Recipe


class TagAdmin(admin.ModelAdmin):
    """Определяет структуру вывода информации о тегах."""

   # inlines = [RecipeInline,]

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


class IngredientsInline(admin.TabularInline):
    model = RecipeIngredients
    extra = 1


class TagsInline(admin.TabularInline):
    model = RecipeTags
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'count_recipes_favorite')
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name', 'author', 'tags')
    empty_value_display = "-пусто-"
    inlines = [
        TagsInline, IngredientsInline
    ]
    readonly_fields = ['count_recipes_favorite']

    def count_recipes_favorite(self, obj):
        return obj.favorite_recipes.count()

    count_recipes_favorite.short_description = 'Популярность'


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
#admin.site.register(Group)
#admin.site.register(Comment)
