from rest_framework import generics

from user.models import UserDAO
from user.serializers import UserSerializer


class UserRestAPI(generics.ListCreateAPIView):
    queryset = UserDAO.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
