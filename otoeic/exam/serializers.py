from rest_framework import serializers

from word.serializers import WordSerializer
from .models import ExamDAO
from .models import ExamQuestionDAO


class ExamQuestionSerializer(serializers.ModelSerializer):
    word = WordSerializer(read_only=True)

    class Meta:
        model = ExamQuestionDAO
        fields = ['word', 'order', 'submitted_answer']


class ExamSubmitSerializer(serializers.Serializer):
    answers = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = ExamDAO
        fields = [
            'answers'
        ]


class ExamSerializer(serializers.ModelSerializer):
    questions = ExamQuestionSerializer(many=True, read_only=True)

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
            'questions',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'point': {'read_only': True},
            'date_created': {'read_only': True},
            'date_submitted': {'read_only': True},
            'questions': {'read_only': True},
        }
