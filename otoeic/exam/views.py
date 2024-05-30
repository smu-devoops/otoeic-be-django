from http import HTTPStatus

from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from . import models
from . import serializers


class IsCreator(permissions.BasePermission):
    def has_object_permission(self, request: Request, view, obj: models.ExamDAO):
        return bool(
            request.user and
            obj.user_created == request.user
        )


class ExamListCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = models.ExamDAO.objects.filter(date_submitted=None)
        if not self.request.user.is_staff:
            queryset = queryset.filter(user_created=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        # 새로 생성된 시험은 문제 목록도 보여줘야 하므로 Serializer를 변경
        serializer = serializers.UnsubmittedExamSerializer(instance=instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UnsubmittedExamRetrieveView(generics.RetrieveAPIView):
    queryset = models.ExamDAO.objects.filter(date_submitted=None)
    serializer_class = serializers.UnsubmittedExamSerializer
    permission_classes = [IsCreator|permissions.IsAdminUser]
    lookup_field = 'id'


class SubmittedExamRetrieveView(generics.RetrieveAPIView):
    queryset = models.ExamDAO.objects.exclude(date_submitted=None)
    serializer_class = serializers.SubmittedExamSerializer
    permission_classes = [IsCreator|permissions.IsAdminUser]
    lookup_field = 'id'


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
