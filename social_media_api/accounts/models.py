from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """
    Custom user model for social media with follow functionality
    """
    # REQUIRED FIELDS from previous tasks:
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    # FOLLOW SYSTEM: Many-to-many relationship to self
    # Task says: "following field, which is a many-to-many relationship to itself"
    following = models.ManyToManyField(
        'self',
        symmetrical=False,  # If A follows B, B doesn't automatically follow A
        blank=True,
        related_name='followers',  # Reverse relation
        through='FollowRelationship'  # Optional: through model for extra data
    )
    
    # Email field
    email = models.EmailField(_('email address'), unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    def __str__(self):
        return self.email
    
    # Helper methods for follow functionality
    def follow(self, user):
        """Follow another user"""
        if user != self and not self.is_following(user):
            self.following.add(user)
    
    def unfollow(self, user):
        """Unfollow a user"""
        if user != self and self.is_following(user):
            self.following.remove(user)
    
    def is_following(self, user):
        """Check if following a user"""
        return self.following.filter(id=user.id).exists()
    
    def get_followers_count(self):
        """Get number of followers"""
        return self.followers.count()
    
    def get_following_count(self):
        """Get number of users being followed"""
        return self.following.count()

# Optional: Through model for follow relationships (can store extra data like timestamp)
class FollowRelationship(models.Model):
    follower = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='follow_relationships'
    )
    following = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='followed_by_relationships'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'following')
    
    def __str__(self):
        return f"{self.follower} follows {self.following}"
