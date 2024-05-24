from rest_framework import serializers

from word.models import Word


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
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