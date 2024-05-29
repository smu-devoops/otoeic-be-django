from django.db import models

from user.models import Level
from user.models import UserDAO


class WordType(models.TextChoices):
    NOUN = 'n', 'noun (명사)'
    PRONOUN = 'pron', 'pronoun (대명사)'
    VERB = 'v', 'verb (동사)'
    ADJECTIVE = 'a', 'adjective (형용사)'
    ADVERB = 'ad', 'adverb (부사)'
    PREPOSITION = 'prep', 'preposition (전치사)'
    CONJUNCTION = 'conj', 'conjunction (접속사)'
    INTERJECTION = 'int', 'interjection (감탄사)'
    IDIOM = 'idm', 'idiom (숙어)'


class WordDAO(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True)
    english = models.TextField(unique=True, null=False, blank=False, editable=False)
    korean = models.TextField(null=False, blank=False)
    type = models.CharField(max_length=5, choices=WordType.choices)
    level = models.IntegerField(choices=Level.choices)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user_created = models.ForeignKey(UserDAO, on_delete=models.CASCADE, null=True) # if Null, it means this word is shared among all users.
