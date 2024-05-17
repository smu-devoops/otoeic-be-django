from rest_framework import generics


from user.models import User
from user.serializers import UserSerializer


class UserRestAPI(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
