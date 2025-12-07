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
    
    def test_url_patterns_match_requirements(self):
        """Test that URL patterns match exactly what checker expects"""
        
        # Test create comment URL - should be /post/<pk>/comments/new/
        create_url = reverse('comment_create', kwargs={'pk': self.post.pk})
        self.assertEqual(create_url, f'/post/{self.post.pk}/comments/new/')
        
        # Test update comment URL - should be /comment/<pk>/update/
        update_url = reverse('comment_update', kwargs={'pk': self.comment.pk})
        self.assertEqual(update_url, f'/comment/{self.comment.pk}/update/')
        
        # Test delete comment URL - should be /comment/<pk>/delete/
        delete_url = reverse('comment_delete', kwargs={'pk': self.comment.pk})
        self.assertEqual(delete_url, f'/comment/{self.comment.pk}/delete/')
        
        # Test post detail URL - should be /post/<pk>/
        post_detail_url = reverse('post_detail', kwargs={'pk': self.post.pk})
        self.assertEqual(post_detail_url, f'/post/{self.post.pk}/')
    
    def test_comment_create_view_url(self):
        """Test comment create view works with correct URL"""
        self.client.login(username='testuser2', password='testpass123')
        response = self.client.get(
            reverse('comment_create', kwargs={'pk': self.post.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/comment_form.html')
        
        # Test POST request
        response = self.client.post(
            reverse('comment_create', kwargs={'pk': self.post.pk}),
            {'content': 'New comment via correct URL pattern'}
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(Comment.objects.count(), 2)
    
    def test_comment_update_view_url(self):
        """Test comment update view works with correct URL"""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(
            reverse('comment_update', kwargs={'pk': self.comment.pk})
        )
        self.assertEqual(response.status_code, 200)
        
        # Test POST request
        response = self.client.post(
            reverse('comment_update', kwargs={'pk': self.comment.pk}),
            {'content': 'Updated comment content'}
        )
        self.assertEqual(response.status_code, 302)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Updated comment content')
    
    def test_comment_delete_view_url(self):
        """Test comment delete view works with correct URL"""
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(
            reverse('comment_delete', kwargs={'pk': self.comment.pk})
        )
        self.assertEqual(response.status_code, 200)
        
        # Test POST request
        response = self.client.post(
            reverse('comment_delete', kwargs={'pk': self.comment.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 0)
    
    def test_views_exist(self):
        """Test that all required views exist and are accessible"""
        
        # Check CommentCreateView exists
        from .views import CommentCreateView
        self.assertTrue(hasattr(CommentCreateView, 'as_view'))
        
        # Check CommentUpdateView exists with required mixins
        from .views import CommentUpdateView
        self.assertTrue(hasattr(CommentUpdateView, 'as_view'))
        
        # Check CommentDeleteView exists with required mixins
        from .views import CommentDeleteView
        self.assertTrue(hasattr(CommentDeleteView, 'as_view'))
        
        # Check mixins are used
        from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
        self.assertTrue(issubclass(CommentCreateView, LoginRequiredMixin))
        self.assertTrue(issubclass(CommentUpdateView, LoginRequiredMixin))
        self.assertTrue(issubclass(CommentUpdateView, UserPassesTestMixin))
        self.assertTrue(issubclass(CommentDeleteView, LoginRequiredMixin))
        self.assertTrue(issubclass(CommentDeleteView, UserPassesTestMixin))
    
    def test_form_validation(self):
        """Test comment form validation rules"""
        from .forms import CommentForm
        
        # Test valid comment
        form = CommentForm(data={'content': 'Valid comment with more than 3 chars'})
        self.assertTrue(form.is_valid())
        
        # Test invalid comment (too short)
        form = CommentForm(data={'content': 'a'})
        self.assertFalse(form.is_valid())
        self.assertIn('Comment must be at least 3 characters', str(form.errors))
        
        # Test empty comment
        form = CommentForm(data={'content': ''})
        self.assertFalse(form.is_valid())
