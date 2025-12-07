from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Comment

class CommentTestCase(TestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='user1', password='test123')
        self.user2 = User.objects.create_user(username='user2', password='test123')
        
        # Create a post
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user1
        )
        
        # Create a comment
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user1,
            content='Test comment'
        )
        
        self.client = Client()
    
    def test_comment_creation(self):
        """Test that a comment can be created"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.user2,
            content='Another test comment'
        )
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.author, self.user2)
    
    def test_comment_edit_permission(self):
        """Test that only comment author can edit"""
        self.client.login(username='user2', password='test123')
        response = self.client.get(reverse('edit_comment', args=[self.comment.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect
    
    def test_comment_delete_permission(self):
        """Test that only comment author can delete"""
        self.client.login(username='user2', password='test123')
        response = self.client.get(reverse('delete_comment', args=[self.comment.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect
    
    def test_authenticated_user_can_comment(self):
        """Test authenticated user can add comment"""
        self.client.login(username='user2', password='test123')
        response = self.client.post(reverse('add_comment', args=[self.post.id]), {
            'content': 'New comment from test'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to post detail
        self.assertEqual(Comment.objects.count(), 2)
    
    def test_unauthenticated_user_cannot_comment(self):
        """Test unauthenticated user cannot add comment"""
        response = self.client.post(reverse('add_comment', args=[self.post.id]), {
            'content': 'Should not work'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to login
