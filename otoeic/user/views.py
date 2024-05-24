from rest_framework import generics

from .models import UserDAO
from .serializers import UserSerializer


class UserRestAPI(generics.ListCreateAPIView):
    queryset = UserDAO.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        queryset = super().get_queryset()
        if self.request.query_params:
            username = self.request.query_params.get('username')
            print(username)
            return queryset.filter(username=username)
        return queryset
