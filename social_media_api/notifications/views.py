from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.pagination import PageNumberPagination

# Step 1: Create a custom pagination class
class NotificationPagination(PageNumberPagination):
    page_size = 10  # Define how many notifications per page (adjust as needed)
    page_size_query_param = 'page_size'  # Allow the client to override page_size via query param
    max_page_size = 100  # Set a maximum page size

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Step 2: Fetch notifications and filter by unread ones
        notifications = Notification.objects.filter(recipient=request.user, is_read=False)

        # Step 3: Paginate the notifications
        paginator = NotificationPagination()
        paginated_notifications = paginator.paginate_queryset(notifications, request)

        # Step 4: Serialize the paginated data
        serializer = NotificationSerializer(paginated_notifications, many=True)

        # Step 5: Return paginated response
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        notification_id = request.data.get('notification_id')
        notification = Notification.objects.get(id=notification_id, recipient=request.user)

        # Mark the notification as read
        notification.is_read = True
        notification.save()

        return Response({"detail": "Notification marked as read."}, status=status.HTTP_200_OK)
