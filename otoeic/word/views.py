from django.db.models import Q
from django.db.transaction import atomic
from rest_framework import request
from rest_framework import generics
from rest_framework import pagination
from rest_framework import permissions
from rest_framework import filters

from user.models import UserDAO
from . import models
from . import serializers


class WordAccessPermission(permissions.BasePermission):
    message = 'Manipulation is not allowed.'

    def has_permission(self, request: request.Request, view: generics.GenericAPIView):
        word: models.WordDAO = view.get_object()
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_staff or
            word.user_created == request.user
        )


class WordListCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.WordSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.PageNumberPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'

    def get_queryset(self):
        return models.WordDAO.objects.filter(Q(user_created=self.request.user) | Q(user_created=None))

    def perform_create(self, serializer):
        word: models.WordDAO
        user: UserDAO
        user = self.request.user
        with atomic():
            word = serializer.save()
            # 관리자가 추가하고 있는 단어이면 공용 단어로 만들기 위해 사용자를 None 으로 지정
            word.user_created = None if user.is_staff else user
            word.save()


class WordManipulateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.WordDAO.objects.all()
    serializer_class = serializers.WordSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, WordAccessPermission]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        self._validate_permission()
        return super().retrieve(request, *args, **kwargs)

    def perform_destroy(self, instance):
        self._validate_permission()
        return super().perform_destroy(instance)

    def perform_update(self, serializer):
        self._validate_permission()
        return super().perform_update(serializer)

    def _validate_permission(self):
        word: models.WordDAO
        word = self.get_object()
        print(self.request.user)
        if word.user_created == self.request.user or self.request.user.is_staff:
            return
        raise PermissionError
