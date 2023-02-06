from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import UniqueConstraint

from users.validators import validate_username


class User(AbstractUser):
    """Модель пользователя."""

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Адрес электронной почты',
    )
    username = models.CharField(
        validators=([validate_username]),
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Уникальный юзернейм',
    )
    first_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name='Фамилия',
    )
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль',
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


#class User(AbstractUser):
#    USERNAME_FIELD = 'email'
#    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']
#
#    username = models.CharField('username', max_length=150, unique=True)
#    password = models.TextField('password', max_length=150)
#    email = models.EmailField('e-mail', max_length=254, unique=True)
#    first_name = models.TextField('first_name', max_length=150)
#    last_name = models.TextField('last_name', max_length=150)
#
#    def __str__(self):
#        return self.username
#
#
class Follow(models.Model):
    """Определяет модель для подписки на авторов."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Кто подписывается',
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='На кого подписывается',
        related_name='following',
    )
    UniqueConstraint(
        fields=['user', 'author'], name='unique_followers'
    )
