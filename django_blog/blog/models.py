from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})
    
    def get_update_url(self):
        return reverse('post_update', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse('post_delete', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ['-published_date']
