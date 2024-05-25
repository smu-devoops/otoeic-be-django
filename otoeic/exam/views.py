from http import HTTPStatus

from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import ExamDAO
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
            exam.post_submit(self.request.data['answers'])
        except AssertionError as e:
            return Response(data={'error': str(e)}, status=HTTPStatus.BAD_REQUEST)
        return Response(data=ExamSerializer(exam).data, status=HTTPStatus.OK)
