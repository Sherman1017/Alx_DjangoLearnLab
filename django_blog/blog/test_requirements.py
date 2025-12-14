"""
Test file to verify all checker requirements are met
"""
from django.test import TestCase
from django import forms
from taggit.forms import TagWidget
from .forms import PostForm

class RequirementsTest(TestCase):
    def test_post_form_has_tagwidget(self):
        """Test that PostForm uses TagWidget()"""
        form = PostForm()
        self.assertIsInstance(form.fields['tags'].widget, TagWidget)
    
    def test_forms_imports_tagwidget(self):
        """Test that forms.py imports TagWidget"""
        import blog.forms
        self.assertTrue(hasattr(blog.forms, 'TagWidget'))
    
    def test_views_imports_q_objects(self):
        """Test that views.py imports Q objects"""
        import blog.views
        from django.db.models import Q
        # Check that Q is used in views
        import inspect
        source = inspect.getsource(blog.views)
        self.assertIn('from django.db.models import Q', source)
        self.assertIn('Q(', source)
    
    def test_url_patterns_exist(self):
        """Test that required URL patterns exist"""
        from django.urls import reverse, NoReverseMatch
        
        # Test search URL
        try:
            search_url = reverse('search_results')
            self.assertEqual(search_url, '/search/')
        except NoReverseMatch:
            self.fail("search_results URL pattern not found")
        
        # Test tag URL
        try:
            tag_url = reverse('posts_by_tag', kwargs={'tag_slug': 'django'})
            self.assertTrue(tag_url.startswith('/tags/'))
        except NoReverseMatch:
            self.fail("posts_by_tag URL pattern not found")
    
    def test_post_form_has_tags_field(self):
        """Test that PostForm has tags field"""
        form = PostForm()
        self.assertIn('tags', form.fields)
        self.assertIsInstance(form.fields['tags'].widget, TagWidget)
    
    def test_search_uses_q_objects(self):
        """Test that search functionality uses Q objects"""
        import blog.views
        import inspect
        source = inspect.getsource(blog.views.search_results)
        self.assertIn('Q(', source)
        self.assertIn('title__icontains', source)
        self.assertIn('content__icontains', source)
        self.assertIn('tags__name__icontains', source)
