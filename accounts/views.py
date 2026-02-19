from django.contrib.auth import get_user_model
from rest_framework import permissions, generics

from .serializers import UserSerializer


User = get_user_model()


class MeView(generics.RetrieveAPIView):
    """
    Simple endpoint to fetch the current authenticated user.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

