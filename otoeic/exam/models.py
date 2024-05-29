from __future__ import annotations

import datetime
from random import shuffle
from typing import Tuple

from django.db import models
from django.db import transaction
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator

from user.models import Level
from user.models import UserDAO
from word.models import WordDAO
from . import utils


DAILY_BONUS_POINT_MULTIPLIER = 3


class ExamDAO(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True)
    level = models.IntegerField(choices=Level.choices)
    amount = models.IntegerField(validators=[MinValueValidator(10), MaxValueValidator(40)])
    ranked = models.BooleanField(default=False)
    point = models.IntegerField(default=0)
    user_created = models.ForeignKey(UserDAO, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True)
    date_submitted = models.DateTimeField(null=True)

    questions: models.QuerySet[ExamQuestionDAO]

    def save(self, **kwargs) -> None:
        is_created = self.pk is None
        with transaction.atomic():
            super().save(**kwargs)
            if is_created:
                self.post_create()

    def post_create(self):
        words = WordDAO.objects.filter(level=self.level)
        words = list(words)
        shuffle(words)
        words = words[:self.amount]
        for order, word in enumerate(words, start=1):
            ExamQuestionDAO.objects.create(exam=self, word=word, order=order)

    def post_submit(self, submitted_answers: Tuple[str]):
        with transaction.atomic():
            assert self.date_submitted is None, (
                'Already submitted.'
            )
            self.date_submitted = datetime.datetime.now()
            self._validate_submitted_answers(submitted_answers)
            self._update_submitted_answers(submitted_answers)
            self._update_point()
            self._update_streak()
            self.save()

    def _validate_submitted_answers(self, submitted_answers: Tuple[str]):
        assert len(self.questions.all()) == len(submitted_answers), (
            'The number of answers does not match the number of questions.'
        )

    def _update_submitted_answers(self, submitted_answers: Tuple[str]):
        for question, answer in zip(self.questions.all(), submitted_answers):
            question.submitted_answer = answer.strip()
            question.save()

    def _update_point(self) -> int:
        today = datetime.datetime.now()
        point = self._count_correct_answers()
        if not self._did_submit_on(today):
            point *= DAILY_BONUS_POINT_MULTIPLIER
        self.point = point
        self.user.point += point

    def _count_correct_answers(self) -> int:
        correct_answers = 0
        for question in self.questions.all():
            if question.word.english.strip() == question.submitted_answer.strip():
                correct_answers += 1
        return correct_answers

    def _update_streak(self):
        today = datetime.datetime.now()
        yesterday = today-datetime.timedelta(days=1)
        if not self._did_submit_on(yesterday):
            self.user.streak = 0
        if self._did_submit_on(today):
            self.user.streak += 1
        self.user.save()

    def _did_submit_on(self, date: datetime.datetime) -> bool:
        return ExamDAO.objects.filter(
            user=self.user,
            date_submitted__range=utils.get_date_range(date)
        ).exists()


class ExamQuestionDAO(models.Model):
    exam = models.ForeignKey(ExamDAO, on_delete=models.CASCADE, related_name='questions')
    word = models.ForeignKey(WordDAO, on_delete=models.PROTECT)
    order = models.IntegerField()
    submitted_answer = models.TextField(blank=True, default='')
