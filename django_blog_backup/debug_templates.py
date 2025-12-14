import os
import sys
import django

sys.path.append('/Alx_DjangoLearnLab/django_blog')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog.settings')
django.setup()

from django.conf import settings
from django.template.loader import get_template

print("Template settings:")
print(f"BASE_DIR: {settings.BASE_DIR}")
print(f"TEMPLATES DIRS: {settings.TEMPLATES[0]['DIRS']}")
print(f"APP_DIRS: {settings.TEMPLATES[0]['APP_DIRS']}")

print("\nLooking for templates...")
template_paths = [
    'blog/home.html',
    'blog/base.html',
    'registration/login.html',  # Django's default auth templates
]

for template in template_paths:
    try:
        t = get_template(template)
        print(f"✅ Found: {template}")
        print(f"   Path: {t.origin.name}")
    except Exception as e:
        print(f"❌ Not found: {template}")
        print(f"   Error: {e}")

print("\nChecking template directories...")
for root, dirs, files in os.walk(settings.BASE_DIR):
    if 'templates' in root:
        print(f"\nTemplates in {root}:")
        for file in files:
            if file.endswith('.html'):
                print(f"  - {file}")
