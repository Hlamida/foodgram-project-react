from django.contrib import admin



from recipes.models import Ingredient, Recipe, Tag


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


#class IngredientInline(admin.TabularInline):
#    model = Ingredient
#    #fk_name = 'recipe_test'


#class TagInline(admin.TabularInline):
#    model = Tag
    #fk_name = 'recipe'


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
#admin.site.register(Recipe, RecipeAdmin)
#admin.site.register(Group)
#admin.site.register(Comment)
