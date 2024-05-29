from django.db.models import Q
from django.db.transaction import atomic
from rest_framework import generics
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from rest_framework.request import Request

from user.models import UserDAO
from . import models
from . import serializers


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsWordOwner(permissions.BasePermission):
    message = 'Not an owner of this word.'

    def has_object_permission(self, request: Request, view, obj: models.WordDAO):
        return bool(
            request.user and
            obj.user_created == request.user
        )


class WordListCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.WordSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [OrderingFilter]
    ordering_fields = '__all__'

    def get_queryset(self):
        return models.WordDAO.objects.filter(Q(user_created=self.request.user) | Q(user_created=None))

    def perform_create(self, serializer):
        word: models.WordDAO
        user: UserDAO = self.request.user
        with atomic():
            word = serializer.save()
            # 관리자가 추가하고 있는 단어이면 공용 단어로 만들기 위해 사용자를 None 으로 지정
            word.user_created = None if user.is_staff else user
            word.save()


class WordManipulateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.WordDAO.objects.all()
    serializer_class = serializers.WordSerializer
    permission_classes = [ReadOnly|IsWordOwner|permissions.IsAdminUser]
    lookup_field = 'id'
