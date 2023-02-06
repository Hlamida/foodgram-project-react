import re
from rest_framework import serializers

from django.core.exceptions import ValidationError


def validate_username(value):
    """Не разрешает имя 'me' при регистрации."""

    if value == 'me':
        raise ValidationError(
            ('Измените имя пользователя.'),
            params={'value': value},
        )

    if re.match(r'^[\\w.@+-]+\\z', value):
        raise serializers.ValidationError(
            'Недопустимые символы в username.'
        )


def validate_hex(value):
    """Проверяет допустимые значения поля HEX."""

    if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value):
        raise serializers.ValidationError(
            'Недопустимый формат HEX.', value,
        )
