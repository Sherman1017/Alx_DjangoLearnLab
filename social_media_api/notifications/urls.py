from django.urls import path
from .views import (
    NotificationListView,
    NotificationDetailView,
    MarkAllNotificationsReadView
)

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification_list'),
    path('<int:pk>/', NotificationDetailView.as_view(), name='notification_detail'),
    path('mark-all-read/', MarkAllNotificationsReadView.as_view(), name='mark_all_read'),
]
