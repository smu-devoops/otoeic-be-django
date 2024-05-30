from http import HTTPStatus

from django.contrib import auth
from rest_framework import exceptions
from rest_framework import filters
from rest_framework import generics
from rest_framework import permissions
from rest_framework import views
from rest_framework.request import Request
from rest_framework.response import Response

from . import models
from . import serializers


class UserListView(generics.ListAPIView):
    queryset = models.UserDAO.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']


class UserRegisterView(generics.CreateAPIView):
    queryset = models.UserDAO.objects.all()
    serializer_class = serializers.UsernamePasswordSerializer
    permission_classes = [permissions.AllowAny]


class UserLoginView(generics.GenericAPIView):
    queryset = models.UserDAO.objects.all()
    serializer_class = serializers.UsernamePasswordSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request: Request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is None:
            auth.logout(request)
            raise exceptions.AuthenticationFailed(detail=(
                f"User authentication failed."
            ))
        auth.login(request, user)
        data = self.get_serializer(instance=user).data
        return Response(data=data, status=HTTPStatus.OK)


class UserLogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, *args, **kwargs):
        auth.logout(request)
        data = { "detail": "Successfully logged out." }
        return Response(data=data, status=HTTPStatus.OK)


class UserManageView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.UserDAO.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'id'


class UserSelfView(generics.GenericAPIView):
    queryset = models.UserDAO.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, *args, **kwargs):
        data = self.get_serializer(self.get_object()).data
        return Response(data, status=HTTPStatus.OK)

    def get_object(self):
        return auth.get_user(self.request)
