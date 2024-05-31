from rest_framework import serializers

from user.serializers import UsernameSerializer
from word.serializers import WordForSubmittedExamSerializer
from word.serializers import WordForUnsubmittedExamSerializer
from . import models


class ExamSerializer(serializers.ModelSerializer):
    user_created = UsernameSerializer(read_only=True)

    class Meta:
        model = models.ExamDAO
        fields = [
            'id',
            'level',
            'amount',
            'point',
            'ranked',
            'user_created',
            'date_created',
            'date_submitted',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'point': {'read_only': True},
            'user_created': {'read_only': True},
            'date_created': {'read_only': True},
            'date_submitted': {'read_only': True},
        }


class UnsubmittedQuestionSerializer(serializers.ModelSerializer):
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
    questions = UnsubmittedQuestionSerializer(many=True, read_only=True)

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
            'level': {'read_only': True},
            'amount': {'read_only': True},
            'ranked': {'read_only': True},
            'user_created': {'read_only': True},
            'date_created': {'read_only': True},
            'questions': {'read_only': True},
        }


class SubmittedQuestionSerializer(serializers.ModelSerializer):
    word = WordForSubmittedExamSerializer(read_only=True)

    class Meta:
        model = models.ExamQuestionDAO
        fields = [
            'word',
            'order',
            'is_correct',
            'answer_submitted',
        ]
        extra_kwargs = {
            'word': {'read_only': True},
            'order': {'read_only': True},
            'is_correct': {'read_only': True},
            'answer_submitted': {'read_only': True},
        }


class SubmittedExamSerializer(serializers.ModelSerializer):
    user_created = UsernameSerializer(read_only=True)
    questions = SubmittedQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = models.ExamDAO
        fields = [
            'id',
            'level',
            'amount',
            'ranked',
            'point',
            'user_created',
            'date_created',
            'date_submitted',
            'questions',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'level': {'read_only': True},
            'amount': {'read_only': True},
            'ranked': {'read_only': True},
            'point': {'read_only': True},
            'user_created': {'read_only': True},
            'date_created': {'read_only': True},
            'date_submitted': {'read_only': True},
            'questions': {'read_only': True},
        }


class SubmittedAnswerListSerializer(serializers.Serializer):
    answers = serializers.ListField(child=serializers.CharField(allow_blank=True))

    class Meta:
        model = models.ExamDAO
        fields = [
            'answers'
        ]
