from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Level(models.IntegerChoices):
    LEVEL_1 = 1, '1'
    LEVEL_2 = 2, '2'
    LEVEL_3 = 3, '3'
    LEVEL_4 = 4, '4'


class User(AbstractUser):
    id = models.IntegerField(primary_key=True, auto_created=True)
    username = models.EmailField(unique=True, null=False, blank=False)
    password = models.EmailField(unique=True, null=False, blank=False)
    level = models.IntegerField(choices=Level.choices, default=Level.LEVEL_1)
    streak_freeze_amount = models.IntegerField(default=0)
    is_streak_freeze_activated = models.BooleanField(default=False)
    point = models.IntegerField(default=0)

    # Django AbstractUser에서 사용하지 않을 기본 필드들 값 설정
    first_name = None
    last_name = None
    email = None
    is_staff = False
    is_active = True
