from django.apps import AppConfig

class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'
    
    def ready(self):
        # Try to import signals, but don't fail if they don't exist yet
        try:
            import notifications.signals
        except ImportError:
            pass
