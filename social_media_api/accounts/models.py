from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """
    Custom user model for social media
    """
    # REQUIRED FIELDS from task:
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    followers = models.ManyToManyField(
        'self', 
        symmetrical=False,
        blank=True, 
        related_name='following'
    )
    
    # Add email field
    email = models.EmailField(_('email address'), unique=True)
    
    # Username is already inherited from AbstractUser, but we need to ensure it's there
    # AbstractUser already has: username, first_name, last_name, email, etc.
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    def __str__(self):
        return self.email
