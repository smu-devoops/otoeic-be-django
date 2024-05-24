from rest_framework import serializers

from .models import ExamDAO
from .models import ExamQuestionDAO


class ExamQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamQuestionDAO
        fields = ['word', 'order', 'submitted_answer']


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamDAO
        fields = [
            'id',
            'user',
            'level',
            'amount',
            'point',
            'date_created',
            'date_submitted',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'point': {'read_only': True},
            'date_created': {'read_only': True},
            'date_submitted': {'read_only': True},
        }
