from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from .models import ExamDAO
from .serializers import ExamSerializer


class ExamListRestAPI(generics.ListCreateAPIView):
    queryset = ExamDAO.objects.all()
    serializer_class = ExamSerializer
    permission_classes = []
    pagination_class = PageNumberPagination


class ExamRestAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExamDAO.objects.all()
    serializer_class = ExamSerializer
    permission_classes = []
    lookup_field = 'id'
