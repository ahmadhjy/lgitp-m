from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Notification
from .serializers import NotificationSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)


# should i put notification details ? i think no
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notification_detail(request, pk):
    try:
        notification = Notification.objects.get(pk=pk, user=request.user)
    except Notification.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = NotificationSerializer(notification)
    return Response(serializer.data)


# ok this one is important
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def mark_notification_as_read(request, pk):
    try:
        notification = Notification.objects.get(pk=pk, user=request.user)
    except Notification.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    notification.read = True
    notification.save()
    return Response(status=status.HTTP_204_NO_CONTENT)
