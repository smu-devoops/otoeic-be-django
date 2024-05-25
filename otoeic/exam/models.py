from __future__ import annotations

from random import shuffle

from django.db import models
from django.db import transaction
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator

from user.models import Level
from user.models import UserDAO
from word.models import WordDAO


DAILY_BONUS_POINT_MULTIPLIER = 3
HOUR_OF_START_OF_THE_DAY = 6


class ExamDAO(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True)
    user = models.ForeignKey(UserDAO, on_delete=models.CASCADE)
    level = models.IntegerField(choices=Level.choices)
    amount = models.IntegerField(validators=[MinValueValidator(10), MaxValueValidator(40)])
    point = models.IntegerField(default=0)
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


class ExamQuestionDAO(models.Model):
    exam = models.ForeignKey(ExamDAO, on_delete=models.CASCADE, related_name='questions')
    word = models.ForeignKey(WordDAO, on_delete=models.PROTECT)
    order = models.IntegerField()
    submitted_answer = models.TextField(blank=True, default='')
