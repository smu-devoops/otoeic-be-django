from http import HTTPStatus

from rest_framework import generics
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.response import Response

from . import models
from . import serializers


class ExamCreateView(generics.ListCreateAPIView):
    queryset = models.ExamDAO.objects.all()
    serializer_class = serializers.UnsubmittedExamSerializer
    permission_classes = [permissions.IsAuthenticated]


class ExamRestAPI(generics.RetrieveUpdateAPIView):
    queryset = models.ExamDAO.objects.all()
    serializer_class = serializers.ExamSerializer
    permission_classes = []
    lookup_field = 'id'


class ExamSubmitRestAPI(generics.GenericAPIView):
    queryset = models.ExamDAO.objects.all()
    serializer_class = serializers.ExamSubmitSerializer
    permission_classes = []
    lookup_field = 'id'

    def post(self, request: Request, *args, **kwargs):
        exam: models.ExamDAO = self.get_object()
        try:
            exam.post_submit(self.request.data['answers'])
        except AssertionError as e:
            return Response(data={'error': str(e)}, status=HTTPStatus.BAD_REQUEST)
        return Response(data=serializers.ExamSerializer(exam).data, status=HTTPStatus.OK)
