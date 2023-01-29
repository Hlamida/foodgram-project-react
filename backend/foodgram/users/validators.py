import re
from rest_framework import serializers
import datetime

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
