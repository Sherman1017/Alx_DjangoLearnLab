import os
import sys
import django

# Setup Django
sys.path.append('/Alx_DjangoLearnLab/django_blog')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog.settings')
django.setup()

print("=== Checker Verification ===")

# 1. Check if blog app is installed
from django.conf import settings
if 'blog' in settings.INSTALLED_APPS:
    print("✅ Blog app is installed in settings.py")
else:
    print("❌ Blog app is NOT installed in settings.py")
    print(f"INSTALLED_APPS: {settings.INSTALLED_APPS}")

# 2. Check Post model implementation
try:
    from blog.models import Post
    print("✅ Post model imported successfully")
    
    # Check fields
    fields = [f.name for f in Post._meta.get_fields()]
    required_fields = ['title', 'content', 'published_date', 'author']
    
    missing_fields = [f for f in required_fields if f not in fields]
    if not missing_fields:
        print("✅ Post model has all required fields")
    else:
        print(f"❌ Post model missing fields: {missing_fields}")
        print(f"Available fields: {fields}")
        
except ImportError as e:
    print(f"❌ Could not import Post model: {e}")
except Exception as e:
    print(f"❌ Error checking Post model: {e}")

# 3. Check database configuration
db_config = settings.DATABASES['default']
if db_config['ENGINE'] == 'django.db.backends.sqlite3':
    print("✅ Database configured as SQLite")
else:
    print(f"❌ Database not configured as SQLite: {db_config['ENGINE']}")

print("\n=== Summary ===")
print("All checks should pass for the checker.")
