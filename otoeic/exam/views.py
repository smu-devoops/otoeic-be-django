import datetime
from http import HTTPStatus

from django.db import transaction
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from user.models import UserDAO
from .models import ExamDAO
from .models import DAILY_BONUS_POINT_MULTIPLIER
from .models import HOUR_OF_START_OF_THE_DAY
from .serializers import ExamSerializer
from .serializers import ExamSubmitSerializer


class ExamListRestAPI(generics.ListCreateAPIView):
    queryset = ExamDAO.objects.all()
    serializer_class = ExamSerializer
    permission_classes = []
    pagination_class = PageNumberPagination


class ExamRestAPI(generics.RetrieveUpdateAPIView):
    queryset = ExamDAO.objects.all()
    serializer_class = ExamSerializer
    permission_classes = []
    lookup_field = 'id'


class ExamSubmitRestAPI(generics.GenericAPIView):
    queryset = ExamDAO.objects.all()
    serializer_class = ExamSubmitSerializer
    permission_classes = []
    lookup_field = 'id'

    def post(self, request: Request, *args, **kwargs):
        exam: ExamDAO = self.get_object()
        try:
            with transaction.atomic():
                assert exam.date_submitted is None, (
                    'Already submitted.'
                )
                exam.date_submitted = datetime.datetime.now()
                self._validate_submitted_answers(exam)
                self._update_submitted_answers(exam)
                self._update_point(exam)
                exam.save()
            return Response(data=ExamSerializer(exam).data, status=HTTPStatus.OK)
        except AssertionError as e:
            return Response(data={'error': str(e)}, status=HTTPStatus.BAD_REQUEST)

    def _validate_submitted_answers(self, exam: ExamDAO):
        assert len(exam.questions.all()) == len(self.request.data['answers']), (
            'The number of answers does not match the number of questions.'
        )

    def _update_submitted_answers(self, exam: ExamDAO):
        for question, answer in zip(exam.questions.all(), self.request.data['answers']):
            question.submitted_answer = answer.strip()
            question.save()

    def _update_point(self, exam: ExamDAO) -> int:
        point = self._count_correct_answers(exam)
        if self._is_first_submit(exam.user):
            point *= DAILY_BONUS_POINT_MULTIPLIER
        exam.point = point
        exam.user.point += point

    def _count_correct_answers(self, exam: ExamDAO) -> int:
        correct_answers = 0
        for question in exam.questions.all():
            if question.word.english.strip() == question.submitted_answer.strip():
                correct_answers += 1
        return correct_answers

    def _is_first_submit(self, user: UserDAO) -> bool:
        return not ExamDAO.objects.filter(
            user=user,
            date_submitted__range=self._get_today_date_range(divide_hour=6)
        ).exists()

    def _get_today_date_range(self, divide_hour=HOUR_OF_START_OF_THE_DAY):
        today: datetime.date
        if datetime.datetime.now().hour >= divide_hour:
            today = datetime.date.today()
        else:
            today = datetime.date.today() - datetime.timedelta(days=1)
        tomorrow = today + datetime.timedelta(days=1)
        date_min = datetime.datetime.combine(today, datetime.time(hour=divide_hour))
        date_max = datetime.datetime.combine(tomorrow, datetime.time(hour=divide_hour))
        return (date_min, date_max)
