from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Level(models.IntegerChoices):
    LEVEL_1 = 1, 'Level 1'
    LEVEL_2 = 2, 'Level 2'
    LEVEL_3 = 3, 'Level 3'
    LEVEL_4 = 4, 'Level 4'


class UserDAO(AbstractUser):
    id = models.BigAutoField(primary_key=True, auto_created=True)
    email = models.EmailField(null=True, default=None) # 사용 안 함.
    username = models.CharField(max_length=200, unique=True, blank=False)
    password = models.CharField(max_length=200, blank=False)
    level = models.IntegerField(choices=Level.choices, default=Level.LEVEL_1)
    point = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    streak_freeze_amount = models.IntegerField(default=0)
    streak_freeze_activated = models.BooleanField(default=False)
    date_streak_should_be_updated = models.DateField(auto_now=True)
    date_created = models.DateTimeField(auto_now=True)

    # Django AbstractUser에서 사용하지 않을 기본 필드들 값 설정
    first_name = None
    last_name = None
    is_active = True
