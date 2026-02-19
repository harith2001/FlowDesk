from django.utils import timezone
from rest_framework import permissions, viewsets, decorators, response

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and manage notifications for the current user.
    """

    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @decorators.action(detail=True, methods=["post"])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.read_at = timezone.now()
        notification.save(update_fields=["read_at"])
        return response.Response(self.get_serializer(notification).data)

