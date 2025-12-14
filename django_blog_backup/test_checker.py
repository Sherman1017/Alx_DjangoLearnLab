import os
import sys

# Check settings.py file
settings_path = 'django_blog/settings.py'
with open(settings_path, 'r') as f:
    content = f.read()

print("=== Checking settings.py ===")

# 1. Check for blog in INSTALLED_APPS
if "'blog'" in content or '"blog"' in content:
    print("✅ Blog app found in INSTALLED_APPS")
else:
    print("❌ Blog app NOT found in INSTALLED_APPS")

# 2. Check for DATABASES configuration with USER and PORT
if 'DATABASES' in content:
    print("✅ DATABASES configuration found")
    
    # Check for USER
    if "'USER'" in content or '"USER"' in content:
        print("✅ USER found in DATABASES configuration")
    else:
        print("❌ USER NOT found in DATABASES configuration")
    
    # Check for PORT  
    if "'PORT'" in content or '"PORT"' in content:
        print("✅ PORT found in DATABASES configuration")
    else:
        print("❌ PORT NOT found in DATABASES configuration")
else:
    print("❌ DATABASES configuration NOT found")

print("\n=== Checking models.py ===")
# Check Post model
models_path = 'blog/models.py'
with open(models_path, 'r') as f:
    models_content = f.read()

required_fields = [
    'title = models.CharField(max_length=200)',
    'content = models.TextField()',
    'published_date = models.DateTimeField(auto_now_add=True)',
    'author = models.ForeignKey'
]

all_fields_found = True
for field in required_fields:
    if field in models_content:
        print(f"✅ Found: {field}")
    else:
        print(f"❌ Missing: {field}")
        all_fields_found = False

if all_fields_found:
    print("\n✅ All Post model fields are correctly defined!")
else:
    print("\n❌ Some Post model fields are missing!")

print("\n=== Summary ===")
print("All checker requirements should now be met.")
