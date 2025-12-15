from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class Notification(models.Model):
    """
    Notification model for user activities
    """
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='actor_notifications',
        null=True,
        blank=True
    )
    verb = models.CharField(max_length=255)  # Action description
    # Generic foreign key for flexibility
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['recipient', 'read']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.actor} {self.verb} - {self.recipient}"
    
    def mark_as_read(self):
        self.read = True
        self.save()
    
    def mark_as_unread(self):
        self.read = False
        self.save()
    
    @classmethod
    def create_notification(cls, recipient, actor=None, verb="", target=None):
        """Helper method to create notifications"""
        notification = cls(
            recipient=recipient,
            actor=actor,
            verb=verb,
            timestamp=timezone.now()
        )
        if target:
            notification.target_content_type = ContentType.objects.get_for_model(target)
            notification.target_object_id = target.id
        notification.save()
        return notification
