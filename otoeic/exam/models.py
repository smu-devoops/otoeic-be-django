from __future__ import annotations

from django.db import models
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator

from user.models import Level
from user.models import UserDAO
from word.models import WordDAO


class ExamDAO(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True)
    level = models.IntegerField(choices=Level.choices)
    amount = models.IntegerField(validators=[MinValueValidator(5), MaxValueValidator(50)])
    ranked = models.BooleanField(default=False)
    point = models.IntegerField(default=0)
    user_created = models.ForeignKey(UserDAO, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True)
    date_submitted = models.DateTimeField(null=True, default=None)

    questions: models.QuerySet[ExamQuestionDAO]


class ExamQuestionDAO(models.Model):
    exam = models.ForeignKey(ExamDAO, on_delete=models.CASCADE, related_name='questions')
    word = models.ForeignKey(WordDAO, on_delete=models.PROTECT)
    order = models.IntegerField()
    is_correct = models.BooleanField(default=False)
    answer_submitted = models.CharField(max_length=200, blank=True, default='')
