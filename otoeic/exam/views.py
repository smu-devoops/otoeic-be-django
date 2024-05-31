from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from . import models
from . import serializers
from . import services


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
        queryset = models.ExamDAO.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user_created=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance: models.ExamDAO = services.create_exam(
            user=request.user,
            validated_serializer=serializer,
        )
        # 새로 생성된 시험은 문제 목록도 보여줘야 하므로 Serializer를 변경
        serializer = serializers.UnsubmittedExamSerializer(instance=instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UnsubmittedExamRetrieveView(generics.RetrieveAPIView):
    queryset = models.ExamDAO.objects.all()
    serializer_class = serializers.UnsubmittedExamSerializer
    permission_classes = [IsCreator | permissions.IsAdminUser]
    lookup_field = 'id'


class ExamSubmitView(generics.GenericAPIView):
    queryset = models.ExamDAO.objects.all()
    serializer_class = serializers.SubmittedAnswerListSerializer
    permission_classes = [IsCreator | permissions.IsAdminUser]
    lookup_field = 'id'

    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = services.create_result(
            exam=self.get_object(),
            answers=serializer.validated_data.get('answers'),
        )
        # 제출된 시험은 채점 결과도 보여줘야 하므로 Serializer를 변경
        serializer = serializers.SubmittedExamSerializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubmittedExamRetrieveView(generics.RetrieveAPIView):
    queryset = models.ExamDAO.objects.exclude(date_submitted=None)
    serializer_class = serializers.SubmittedExamSerializer
    permission_classes = [IsCreator | permissions.IsAdminUser]
    lookup_field = 'id'
