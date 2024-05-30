import random
import typing

from django.db.transaction import atomic

from word.models import WordDAO
from . import models


DAILY_BONUS_POINT_MULTIPLIER = 3


def create_questions(exam: models.ExamDAO, shuffle=True):
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
            question.full_clean()
            question.save()


def create_result(exam: models.ExamDAO, answers: typing.List[str]):
    questions = exam.questions.order_by(models.ExamQuestionDAO.order)
    assert len(questions) == len(answers), (
        f'Number of answers({len(answers)}) does not match with number of questions({len(questions)}).'
    )
    with atomic():
        for question, answer in zip(questions, answers):
            question.answer_submitted = answer
            question.is_correct = bool(question.word.english == answer)
            question.full_clean()
            question.save()
        # TODO: give more points for today's first exam
        result = models.ExamResultDAO.objects.create(
            exam=exam,
            points=exam.questions.filter(is_correct=True).count(),
        )
        # TODO: 사용자 수준 점검 관련 기능 추가
        result.full_clean()
        result.save()
