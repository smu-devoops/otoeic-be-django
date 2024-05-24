from django.db import models
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator

from user.models import Level
from user.models import UserDAO
from word.models import WordDAO


class ExamDAO(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True)
    user = models.ForeignKey(UserDAO, on_delete=models.CASCADE)
    level = models.IntegerField(choices=Level.choices)
    amount = models.IntegerField(validators=[MinValueValidator(10), MaxValueValidator(40)])
    point = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now=True)
    date_submitted = models.DateTimeField(null=True)


class ExamQuestionDAO(models.Model):
    exam = models.ForeignKey(ExamDAO, on_delete=models.CASCADE)
    word = models.ForeignKey(WordDAO, on_delete=models.PROTECT)
    order = models.IntegerField()
    submitted_answer = models.TextField(blank=True, default='')
