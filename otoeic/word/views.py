from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from word.models import WordDAO
from word.serializers import WordSerializer


class WordListRestAPI(generics.ListCreateAPIView):
    queryset = WordDAO.objects
    serializer_class = WordSerializer
    permission_classes = []
    pagination_class = PageNumberPagination


class WordRestAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = WordDAO.objects
    serializer_class = WordSerializer
    permission_classes = []
    lookup_field = 'id'
