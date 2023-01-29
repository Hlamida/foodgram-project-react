from django.contrib import admin



from recipes.models import Ingredient, Tag


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
        'quantity',
        'measurement_units',
    )
    search_fields = ('name',)


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
#admin.site.register(Group)
#admin.site.register(Comment)
