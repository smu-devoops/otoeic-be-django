from http import HTTPStatus

from django.contrib import auth
from rest_framework import filters
from rest_framework import generics
from rest_framework import permissions
from rest_framework import request
from rest_framework import response
from rest_framework import views

from . import models
from . import serializers


class UserListView(generics.ListAPIView):
    queryset = models.UserDAO.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']


class UserRegisterView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request: request.Request, *args, **kwargs):
        serializer = serializers.UsernamePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        if models.UserDAO.objects.filter(username=username).exists():
            data = { "detail": "User already exists" }
            return response.Response(data=data, status=HTTPStatus.BAD_REQUEST)

        user = models.UserDAO.objects.create(username=username, password=password)
        user.set_password(password)
        user.save()

        data = serializers.UserSerializer(user).data
        return response.Response(data=data, status=HTTPStatus.CREATED)


class UserLoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request: request.Request, *args, **kwargs):
        serializer = serializers.UsernamePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            data = serializers.UserSerializer(user).data
            return response.Response(data=data, status=HTTPStatus.OK)
        else:
            data = { "detail": "Not authenticated." }
            return response.Response(data=data, status=HTTPStatus.UNAUTHORIZED)


class UserLogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: request.Request, *args, **kwargs):
        auth.logout(request)
        data = { "detail": "Successfully logged out." }
        return response.Response(data=data, status=HTTPStatus.OK)


class UserManageView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.UserDAO.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'id'


class UserSelfView(generics.GenericAPIView):
    queryset = models.UserDAO.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: request.Request, *args, **kwargs):
        data = self.get_serializer(self.get_object()).data
        return response.Response(data, status=HTTPStatus.OK)

    def get_object(self):
        return auth.get_user(self.request)
