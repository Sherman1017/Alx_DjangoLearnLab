from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Comment, Tag

class TaggingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create tags
        self.tag1 = Tag.objects.create(name='django', slug='django')
        self.tag2 = Tag.objects.create(name='python', slug='python')
        
        # Create post with tags
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )
        self.post.tags.add(self.tag1, self.tag2)
        
        self.client = Client()
    
    def test_tag_model(self):
        """Test Tag model creation"""
        self.assertEqual(str(self.tag1), 'django')
        self.assertEqual(self.tag1.slug, 'django')
    
    def test_post_with_tags(self):
        """Test post can have multiple tags"""
        self.assertEqual(self.post.tags.count(), 2)
        self.assertIn(self.tag1, self.post.tags.all())
        self.assertIn(self.tag2, self.post.tags.all())
    
    def test_tag_url_pattern(self):
        """Test tag URL pattern exists"""
        url = reverse('posts_by_tag', kwargs={'slug': 'django'})
        self.assertEqual(url, '/tags/django/')
    
    def test_posts_by_tag_view(self):
        """Test posts_by_tag view"""
        response = self.client.get(reverse('posts_by_tag', kwargs={'slug': 'django'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/posts_by_tag.html')
        self.assertIn('tag', response.context)
        self.assertEqual(response.context['tag'].name, 'django')

class SearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create tags
        tag = Tag.objects.create(name='django', slug='django')
        
        # Create posts for search
        self.post1 = Post.objects.create(
            title='Django Tutorial',
            content='Learn Django framework',
            author=self.user
        )
        self.post1.tags.add(tag)
        
        self.post2 = Post.objects.create(
            title='Python Basics',
            content='Python programming language',
            author=self.user
        )
        
        self.client = Client()
    
    def test_search_url(self):
        """Test search URL pattern"""
        url = reverse('search_results')
        self.assertEqual(url, '/search/')
    
    def test_search_view(self):
        """Test search_results view"""
        response = self.client.get(reverse('search_results'), {'q': 'django'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/search_results.html')
        self.assertIn('query', response.context)
        self.assertEqual(response.context['query'], 'django')
    
    def test_search_functionality(self):
        """Test search finds posts by title"""
        response = self.client.get(reverse('search_results'), {'q': 'tutorial'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['posts'].count(), 1)
        self.assertEqual(response.context['posts'].first().title, 'Django Tutorial')
    
    def test_search_by_tag(self):
        """Test search finds posts by tag"""
        response = self.client.get(reverse('search_results'), {'q': 'django'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['posts'].count(), 1)
    
    def test_empty_search(self):
        """Test search with empty query"""
        response = self.client.get(reverse('search_results'), {'q': ''})
        self.assertEqual(response.status_code, 200)
        self.assertIn('No results found' or 'Enter a search term', response.content.decode())

class PostFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_post_form_with_tags(self):
        """Test post form accepts tags"""
        from .forms import PostForm
        
        form_data = {
            'title': 'New Post',
            'content': 'Post content',
            'tag_names': 'django, python, web'
        }
        
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        # Test tag cleaning
        cleaned_tags = form.cleaned_data['tag_names']
        self.assertEqual(len(cleaned_tags), 3)
        self.assertIn('django', cleaned_tags)
        self.assertIn('python', cleaned_tags)
        self.assertIn('web', cleaned_tags)
    
    def test_post_creation_with_tags(self):
        """Test creating a post with tags via form"""
        response = self.client.post(reverse('post_create'), {
            'title': 'Test Post with Tags',
            'content': 'This is a test post',
            'tag_names': 'test, django, python'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Verify post was created
        post = Post.objects.get(title='Test Post with Tags')
        self.assertEqual(post.tags.count(), 3)
        
        # Verify tags were created
        tag_names = [tag.name for tag in post.tags.all()]
        self.assertIn('test', tag_names)
        self.assertIn('django', tag_names)
        self.assertIn('python', tag_names)
