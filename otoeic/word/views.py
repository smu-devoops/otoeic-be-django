from rest_framework import generics
from rest_framework import pagination
from rest_framework import filters

from .models import WordDAO
from .serializers import WordSerializer


class WordListRestAPI(generics.ListCreateAPIView):
    queryset = WordDAO.objects.all()
    serializer_class = WordSerializer
    permission_classes = []
    pagination_class = pagination.PageNumberPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'


class WordRestAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = WordDAO.objects
    serializer_class = WordSerializer
    permission_classes = []
    lookup_field = 'id'
