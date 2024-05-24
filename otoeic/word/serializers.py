from rest_framework import serializers

from .models import WordDAO


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordDAO
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
        }
