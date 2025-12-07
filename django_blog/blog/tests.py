from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Comment

class CommentTests(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            username='testuser1', 
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2', 
            password='testpass123'
        )
        
        # Create test post
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content for the post',
            author=self.user1
        )
        
        # Create test comment
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user1,
            content='Test comment content'
        )
        
        self.client = Client()
    
    def test_comment_model_str(self):
        """Test Comment model string representation"""
        self.assertEqual(
            str(self.comment),
            f'Comment by {self.user1} on {self.post.title}'
        )
    
    def test_comment_create_view_authenticated(self):
        """Test authenticated user can access comment create view"""
        self.client.login(username='testuser2', password='testpass123')
        response = self.client.get(
            reverse('comment_create', kwargs={'post_id': self.post.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/comment_form.html')
    
    def test_comment_create_view_unauthenticated(self):
        """Test unauthenticated user redirected from comment create view"""
        response = self.client.get(
            reverse('comment_create', kwargs={'post_id': self.post.pk})
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_comment_update_view_author(self):
        """Test comment author can access update view"""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(
            reverse('comment_edit', kwargs={'pk': self.comment.pk})
        )
        self.assertEqual(response.status_code, 200)
    
    def test_comment_update_view_non_author(self):
        """Test non-author cannot access update view"""
        self.client.login(username='testuser2', password='testpass123')
        response = self.client.get(
            reverse('comment_edit', kwargs={'pk': self.comment.pk})
        )
        self.assertEqual(response.status_code, 403)  # Forbidden
    
    def test_comment_delete_view_author(self):
        """Test comment author can access delete view"""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(
            reverse('comment_delete', kwargs={'pk': self.comment.pk})
        )
        self.assertEqual(response.status_code, 200)
    
    def test_comment_delete_view_non_author(self):
        """Test non-author cannot access delete view"""
        self.client.login(username='testuser2', password='testpass123')
        response = self.client.get(
            reverse('comment_delete', kwargs={'pk': self.comment.pk})
        )
        self.assertEqual(response.status_code, 403)  # Forbidden
    
    def test_url_patterns_exist(self):
        """Test that required URL patterns exist"""
        # Test create comment URL pattern
        create_url = reverse('comment_create', kwargs={'post_id': 1})
        self.assertTrue('/posts/1/comments/new/' in create_url)
        
        # Test edit comment URL pattern
        edit_url = reverse('comment_edit', kwargs={'pk': 1})
        self.assertTrue('/comments/1/edit/' in edit_url)
        
        # Test delete comment URL pattern
        delete_url = reverse('comment_delete', kwargs={'pk': 1})
        self.assertTrue('/comments/1/delete/' in delete_url)
    
    def test_comment_form_validation(self):
        """Test comment form validation"""
        from .forms import CommentForm
        
        # Test valid comment
        form = CommentForm(data={'content': 'Valid comment content'})
        self.assertTrue(form.is_valid())
        
        # Test too short comment
        form = CommentForm(data={'content': 'a'})
        self.assertFalse(form.is_valid())
        self.assertIn('Comment must be at least 3 characters', str(form.errors))
