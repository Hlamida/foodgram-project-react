from django.contrib import admin

from users.models import Follow, User


class FollowAdmin(admin.ModelAdmin):
    """Определяет структуру вывода информации о подписчиках."""

    list_display = (
        'user',
        'author',
    )
    list_filter = (
        'user',
        'author',
    )
    search_fields = ('user',)


class UsersAdmin(admin.ModelAdmin):
    """Определяет структуру вывода информации о пользователях."""

    list_display = (
        'username',
        'password',
        'first_name',
        'last_name',
        'email',
    )
    list_filter = (
        'username',
        'email',
    )
    search_fields = ('username',)


admin.site.register(Follow, FollowAdmin)
admin.site.register(User, UsersAdmin)
