"""
Tests for tagging and search functionality
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post

class TaggingSearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create a post with tags
        self.post = Post.objects.create(
            title='Django Tutorial',
            content='Learn Django web framework',
            author=self.user
        )
        self.post.tags.add('django', 'python', 'tutorial')
    
    def test_settings_contains_taggit(self):
        """Test that settings.py contains 'taggit' in INSTALLED_APPS"""
        from django.conf import settings
        self.assertIn('taggit', settings.INSTALLED_APPS)
    
    def test_post_form_has_tags_field(self):
        """Test that PostForm has tags field"""
        from .forms import PostForm
        form = PostForm()
        self.assertIn('tags', form.fields)
    
    def test_search_functionality(self):
        """Test search functionality works"""
        response = self.client.get(reverse('search_results'), {'q': 'django'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/search_results.html')
        self.assertContains(response, 'Django Tutorial')
    
    def test_tag_url_pattern(self):
        """Test tag URL pattern exists"""
        response = self.client.get(reverse('posts_by_tag', kwargs={'tag_slug': 'django'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/posts_by_tag.html')
    
    def test_post_with_tags(self):
        """Test post can have tags"""
        self.assertEqual(self.post.tags.count(), 3)
        self.assertIn('django', self.post.tags.names())
    
    def test_search_by_tag(self):
        """Test search finds posts by tag"""
        response = self.client.get(reverse('search_results'), {'q': 'python'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Tutorial')
    
    def test_home_page_has_search(self):
        """Test home page loads with search"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')
        self.assertContains(response, 'Search')
