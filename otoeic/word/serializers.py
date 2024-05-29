from rest_framework import serializers

from user.serializers import UsernameSerializer
from . import models


class WordSerializer(serializers.ModelSerializer):
    user_created = UsernameSerializer(read_only=True)

    class Meta:
        model = models.WordDAO
        fields = [
            'id',
            'english',
            'korean',
            'type',
            'level',
            'date_modified',
            'date_created',
            'user_created',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'date_created': {'read_only': True},
            'date_modified': {'read_only': True},
            'user_created': {'read_only': True},
        }
