from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Notification
from .serializers import NotificationSerializer, NotificationUpdateSerializer

class NotificationListView(generics.ListAPIView):
    """
    View to list user's notifications
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['timestamp', 'read']
    ordering = ['-timestamp']  # Newest first by default
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # Get counts
        total = queryset.count()
        unread = queryset.filter(read=False).count()
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data['counts'] = {
                'total': total,
                'unread': unread
            }
            return response
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'notifications': serializer.data,
            'counts': {
                'total': total,
                'unread': unread
            }
        })

class NotificationDetailView(generics.RetrieveUpdateAPIView):
    """
    View to retrieve or update a notification
    """
    serializer_class = NotificationUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
    
    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        return obj
    
    def update(self, request, *args, **kwargs):
        # Mainly used to mark as read/unread
        notification = self.get_object()
        serializer = self.get_serializer(notification, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'message': 'Notification updated successfully',
            'notification': NotificationSerializer(notification).data
        })

class MarkAllNotificationsReadView(generics.GenericAPIView):
    """
    View to mark all notifications as read
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        updated = Notification.objects.filter(
            recipient=request.user, 
            read=False
        ).update(read=True)
        
        return Response({
            'message': f'Marked {updated} notifications as read',
            'updated_count': updated
        }, status=status.HTTP_200_OK)

# Signal handlers for automatic notifications
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from posts.models import Comment, Like
from accounts.models import CustomUser

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    """Create notification when someone comments on a post"""
    if created and instance.post.author != instance.author:
        Notification.create_notification(
            recipient=instance.post.author,
            actor=instance.author,
            verb="commented on your post",
            target=instance.post
        )

@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    """Create notification when someone likes a post"""
    if created and instance.post.author != instance.user:
        Notification.create_notification(
            recipient=instance.post.author,
            actor=instance.user,
            verb="liked your post",
            target=instance.post
        )

@receiver(post_save, sender=CustomUser)
def create_follow_notification(sender, instance, created, **kwargs):
    """Create notification when someone follows a user"""
    # This would be triggered from the follow system we already have
    pass
