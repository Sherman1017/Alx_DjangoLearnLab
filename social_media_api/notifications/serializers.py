from rest_framework import serializers
from .models import Notification
from accounts.serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model"""
    actor = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    target = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'target', 
                 'read', 'timestamp']
        read_only_fields = ['timestamp']
    
    def get_target(self, obj):
        # Return basic info about the target object
        if obj.target:
            return {
                'type': obj.target_content_type.model,
                'id': obj.target_object_id,
                'repr': str(obj.target)
            }
        return None

class NotificationUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating notifications (mark as read/unread)"""
    class Meta:
        model = Notification
        fields = ['read']
