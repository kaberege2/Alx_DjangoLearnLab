from django.urls import path
from notifications import views

urlpatterns = [
    path('notifications/', views.NotificationListView.as_view(), name='get_notifications'),
]
