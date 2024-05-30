import datetime
import random
import typing

from django.db.transaction import atomic
from rest_framework import exceptions

from user.models import UserDAO
from word.models import WordDAO
from . import models
from . import serializers


DAILY_BONUS_POINT_MULTIPLIER = 3


def create_exam(user: UserDAO, validated_serializer: serializers.ExamSerializer) -> models.ExamDAO:
    with atomic():
        exam: models.ExamDAO = validated_serializer.save(user_created=user)
        create_questions(
            exam=exam,
            shuffle=True,
        )
        exam.full_clean(exclude=[
            'date_submitted'
        ])
    return exam


def create_questions(exam: models.ExamDAO, shuffle=True) -> models.ExamDAO:
    assert exam.questions.count() == 0, (
        f'This exam already have {exam.questions.count()} questions.'
    )
    words = list(WordDAO.objects.filter(level=exam.level))
    if shuffle:
        random.shuffle(words)
    with atomic():
        for order in range(1, exam.amount+1):
            word = words.pop()
            word.full_clean(exclude=['user_created'])
            question = models.ExamQuestionDAO.objects.create(
                exam=exam,
                word=word,
                order=order,
            )
            question.full_clean(exclude=[
                'answer_submitted'
            ])
            question.save()
    return exam


def create_result(exam: models.ExamDAO, answers: typing.List[str]) -> models.ExamDAO:
    if exam.date_submitted is not None:
        raise exceptions.ValidationError(detail=(
            f'{exam} is already submitted.'
        ))

    if len(answers) != exam.amount:
        raise exceptions.ValidationError(detail=(
            f'{len(answers)} answers given while there are {exam.amount} questions.'
        ))

    with atomic():
        # 제출 일시 갱신
        exam.date_submitted = datetime.datetime.now()

        # 제출된 정답들을 갱신
        for question, answer in zip(exam.questions.order_by('order').all(), answers):
            question.answer_submitted = answer
            question.is_correct = bool(
                question.word.english == answer
            )
            question.full_clean()
            question.save()

        # 시험 성적에 맞게 포인트 업데이트
        earned_point = exam.questions.filter(is_correct=True).count()
        if should_get_bonus(exam):
            earned_point *= DAILY_BONUS_POINT_MULTIPLIER
        earned_point -= exam.point
        exam.point += earned_point
        exam.user_created.point += earned_point
        exam.user_created.full_clean(exclude=['email'])
        exam.user_created.save()

        # TODO: 사용자 수준 점검 관련 기능 추가 (ranked 이면 어떻게 할지...)

        exam.full_clean()
        exam.save()
    return exam


def should_get_bonus(exam: models.ExamDAO) -> bool:
    return True
