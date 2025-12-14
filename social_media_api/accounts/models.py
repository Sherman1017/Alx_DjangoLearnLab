from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # REQUIRED FIELDS:
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, blank=True)
    
    def __str__(self):
        return self.username
