import os
import sys
import django

# Setup Django
sys.path.append('/Alx_DjangoLearnLab/django_blog')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog.settings')
django.setup()

from blog.views import PostCreateView, PostUpdateView, PostDeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

print("=== Testing Mixin Implementation ===")

# Check PostCreateView
print("\n1. Checking PostCreateView...")
if issubclass(PostCreateView, LoginRequiredMixin):
    print("✅ PostCreateView uses LoginRequiredMixin")
else:
    print("❌ PostCreateView does NOT use LoginRequiredMixin")

# Check PostUpdateView
print("\n2. Checking PostUpdateView...")
if issubclass(PostUpdateView, LoginRequiredMixin):
    print("✅ PostUpdateView uses LoginRequiredMixin")
else:
    print("❌ PostUpdateView does NOT use LoginRequiredMixin")

if issubclass(PostUpdateView, UserPassesTestMixin):
    print("✅ PostUpdateView uses UserPassesTestMixin")
else:
    print("❌ PostUpdateView does NOT use UserPassesTestMixin")

# Check PostDeleteView
print("\n3. Checking PostDeleteView...")
if issubclass(PostDeleteView, LoginRequiredMixin):
    print("✅ PostDeleteView uses LoginRequiredMixin")
else:
    print("❌ PostDeleteView does NOT use LoginRequiredMixin")

if issubclass(PostDeleteView, UserPassesTestMixin):
    print("✅ PostDeleteView uses UserPassesTestMixin")
else:
    print("❌ PostDeleteView does NOT use UserPassesTestMixin")

print("\n=== Mixin Test Complete ===")
print("\nAll CRUD views should use:")
print("✅ LoginRequiredMixin - for authentication")
print("✅ UserPassesTestMixin - for author-only access (update/delete)")
