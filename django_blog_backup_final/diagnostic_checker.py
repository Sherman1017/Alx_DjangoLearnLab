import os
import sys
import django
from pathlib import Path

print("=== CHECKER DIAGNOSTIC ===")
print("Looking for EXACT patterns the checker wants...")

# 1. First, check if we're in the right place
print("\n1. Current directory:", os.getcwd())
print("Directory exists:", os.path.exists('.'))

# 2. Check ALL files in the project
print("\n2. Project structure:")
for root, dirs, files in os.walk('.'):
    # Skip hidden directories
    dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'venv', '.git']]
    level = root.replace('.', '').count(os.sep)
    indent = ' ' * 2 * level
    print(f'{indent}{os.path.basename(root)}/')
    subindent = ' ' * 2 * (level + 1)
    for file in files:
        if file.endswith(('.py', '.html', '.md')):
            print(f'{subindent}{file}')

# 3. Check EXACTLY what's in blog/urls.py
print("\n3. Checking blog/urls.py EXACT content:")
with open('blog/urls.py', 'r') as f:
    urls_content = f.read()
    print(urls_content)

# 4. Check EXACTLY what's in blog/views.py
print("\n\n4. Checking blog/views.py for mixins (EXACT lines):")
with open('blog/views.py', 'r') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if 'class Post' in line or 'LoginRequiredMixin' in line or 'UserPassesTestMixin' in line:
            print(f"Line {i+1}: {line.rstrip()}")

# 5. Check templates directory structure
print("\n\n5. Checking templates directory:")
templates_dir = 'templates/blog'
if os.path.exists(templates_dir):
    for file in os.listdir(templates_dir):
        if file.endswith('.html'):
            print(f"  - {file}")
            # Check first few lines
            with open(os.path.join(templates_dir, file), 'r') as f:
                first_lines = [f.readline().strip() for _ in range(3)]
                print(f"    Starts with: {' | '.join(first_lines)}")
else:
    print(f"  ERROR: {templates_dir} does not exist!")

# 6. Try to import Django and check
print("\n\n6. Testing Django setup:")
try:
    sys.path.insert(0, os.getcwd())
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog.settings')
    django.setup()
    
    from django.urls import get_resolver
    resolver = get_resolver()
    
    print("URL patterns found:")
    for pattern in resolver.url_patterns:
        if hasattr(pattern, 'name') and pattern.name:
            print(f"  - {pattern.name}: {pattern.pattern}")
    
    print("\n✅ Django setup successful")
except Exception as e:
    print(f"❌ Django setup failed: {e}")

print("\n=== DIAGNOSTIC COMPLETE ===")
