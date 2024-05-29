from rest_framework import serializers
from rest_framework.request import Request

from user.models import UserDAO
from user.serializers import UsernameSerializer
from word.serializers import WordSerializer
from word.serializers import WordForUnsubmittedExamSerializer
from . import models
from . import services


class QuestionSerializer(serializers.ModelSerializer):
    word = WordForUnsubmittedExamSerializer(read_only=True)

    class Meta:
        model = models.ExamQuestionDAO
        fields = [
            'word',
            'order',
        ]
        extra_kwargs = {
            'word': {'read_only': True},
            'order': {'read_only': True},
        }


class UnsubmittedExamSerializer(serializers.ModelSerializer):
    user_created = UsernameSerializer(read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = models.ExamDAO
        fields = [
            'id',
            'level',
            'amount',
            'ranked',
            'user_created',
            'date_created',
            'questions',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'user_created': {'read_only': True},
            'date_created': {'read_only': True},
            'questions': {'read_only': True},
        }

    def create(self, validated_data):
        request: Request = self.context.get('request')
        assert request.user.is_authenticated, (
            f'Could not find user {request.user}.'
        )
        validated_data['user_created'] = request.user
        exam: models.ExamDAO = super().create(validated_data)
        services.create_questions(exam, shuffle=True)
        return exam


class ExamQuestionSerializer(serializers.ModelSerializer):
    word = WordSerializer(read_only=True)

    class Meta:
        model = models.ExamQuestionDAO
        fields = ['word', 'order', 'submitted_answer']


class ExamSubmitSerializer(serializers.Serializer):
    answers = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = models.ExamDAO
        fields = [
            'answers'
        ]


class ExamSerializer(serializers.ModelSerializer):
    questions = ExamQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = models.ExamDAO
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
